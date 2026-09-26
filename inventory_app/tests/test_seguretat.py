"""Tests de seguretat de l'aplicació d'inventari (revisió del 26/09/2026)."""
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from inventory_app.models import Inventario
from users.models import CustomUser

MEDIA_TMP = tempfile.mkdtemp(prefix="inv-media-")


@override_settings(
    MEDIA_ROOT=MEDIA_TMP,
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    LOGIN_MAX_ATTEMPTS=3,
    LOGIN_MAX_ATTEMPTS_PER_USER=6,
)
class SeguretatTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TMP, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.admin = CustomUser.objects.create_user("gestor", password="Contrasenya-Llarga-42", role="admin")
        self.viewer = CustomUser.objects.create_user("lector", password="Contrasenya-Llarga-42", role="viewer")

    def login(self, username="gestor", password="Contrasenya-Llarga-42", ip="203.0.113.10"):
        return self.client.post(reverse("login"), {"username": username, "password": password},
                                HTTP_X_REAL_IP=ip)

    # --- Configuració -------------------------------------------------------
    def test_debug_desactivat_per_defecte(self):
        self.assertFalse(settings.DEBUG)

    def test_cookies_segures_i_hsts_en_produccio(self):
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)
        self.assertGreater(settings.SECURE_HSTS_SECONDS, 0)
        self.assertEqual(settings.SECURE_PROXY_SSL_HEADER, ("HTTP_X_FORWARDED_PROTO", "https"))

    def test_ruta_inexistent_no_mostra_pagina_de_depuracio(self):
        resp = self.client.get("/ruta-que-no-existeix/")
        self.assertEqual(resp.status_code, 404)
        self.assertNotIn(b"URLconf", resp.content)

    def test_admin_de_django_desactivat(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 404)

    def test_healthz_public(self):
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b"ok")

    # --- Login ----------------------------------------------------------------
    def test_login_correcte_redirigeix(self):
        resp = self.login()
        self.assertRedirects(resp, reverse("dashboard"), fetch_redirect_response=False)

    def test_login_fallit_retorna_401(self):
        self.assertEqual(self.login(password="dolenta").status_code, 401)

    def test_bloqueig_per_ip_despres_de_massa_intents(self):
        for _ in range(3):
            self.login(password="dolenta")
        # Bloquejat encara que ara la contrasenya sigui correcta
        resp = self.login()
        self.assertEqual(resp.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)
        # Una altra IP amb un altre usuari no queda afectada
        self.assertEqual(self.login(username="lector", ip="198.51.100.7").status_code, 302)

    def test_bloqueig_per_usuari_encara_que_canviin_les_ips(self):
        for i in range(6):
            self.login(password="dolenta", ip=f"192.0.2.{i}")
        self.assertEqual(self.login(ip="192.0.2.200").status_code, 429)

    def test_uns_quants_intents_d_un_tercer_no_bloquegen_el_compte(self):
        # Algú des d'una altra IP falla fins al límit per IP...
        for _ in range(3):
            self.login(password="dolenta", ip="203.0.113.99")
        # ...i el titular del compte encara pot entrar des de la seva IP
        self.assertEqual(self.login(ip="198.51.100.20").status_code, 302)

    def test_login_correcte_reinicia_el_comptador(self):
        self.login(password="dolenta")
        self.login(password="dolenta")
        self.assertEqual(self.login().status_code, 302)
        self.client.post(reverse("logout"))
        self.login(password="dolenta")
        self.assertEqual(self.login().status_code, 302)

    def test_logout_nomes_per_post(self):
        self.client.force_login(self.viewer)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.client.post(reverse("logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    # --- Media (fotos i QR) --------------------------------------------------
    def _fitxer_media(self):
        path = Path(MEDIA_TMP) / "qr_codes" / "qr_PROVA.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\x89PNG\r\n\x1a\nprova")
        return "/media/qr_codes/qr_PROVA.png"

    def test_media_requereix_login(self):
        url = self._fitxer_media()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp["Location"])

    def test_media_accessible_amb_login(self):
        url = self._fitxer_media()
        self.client.force_login(self.viewer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("private", resp["Cache-Control"])

    def test_media_rebutja_path_traversal(self):
        self.client.force_login(self.viewer)
        for url in ("/media/../config/settings.py", "/media/%2e%2e/config/settings.py"):
            resp = self.client.get(url)
            # Django respon 400 (SuspiciousFileOperation) o 404: mai el fitxer
            self.assertIn(resp.status_code, (400, 404), url)
            self.assertNotIn(b"SECRET_KEY", resp.content)

    # --- Funcionalitat afectada per l'actualització de dependències ----------
    def test_generacio_d_etiquetes_i_pdf(self):
        self.client.force_login(self.admin)
        resp = self.client.post(reverse("generar_etiquetas"), {"cantidad": 3})
        self.assertRedirects(resp, reverse("descargar_etiquetas_pdf"), fetch_redirect_response=False)
        self.assertEqual(Inventario.objects.count(), 3)
        self.assertTrue(all(i.qr_code for i in Inventario.objects.all()))
        pdf = self.client.get(reverse("descargar_etiquetas_pdf"))
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))

    def test_rols_es_respecten(self):
        self.client.force_login(self.viewer)
        resp = self.client.get(reverse("user_list"))
        self.assertRedirects(resp, reverse("dashboard"), fetch_redirect_response=False)
