# Laporan hasil UTS ? Laravel Blade Layouting

Tanggal pengujian: 28 Oktober 2026, lingkungan Windows / PHP 8.2.12.

## A. Enam halaman Admin

| HTML asli / view Blade | URL | Named route | Method Controller |
| --- | --- | --- | --- |
| `index.html` ? `admin/index.blade.php` | `/admin` | `admin.index` | `index()` |
| `advance-sweet-alert.html` ? `admin/advance-sweet-alert.blade.php` | `/admin/advance-sweet-alert` | `admin.advance-sweet-alert` | `sweetAlert()` |
| `auth-login.html` ? `admin/auth-login.blade.php` | `/admin/auth-login` | `admin.auth-login` | `login()` |
| `calendar.html` ? `admin/calendar.blade.php` | `/admin/calendar` | `admin.calendar` | `calendar()` |
| `form-elements.html` ? `admin/form-elements.blade.php` | `/admin/form-elements` | `admin.form-elements` | `formElements()` |
| `tables-datatable.html` ? `admin/tables-datatable.blade.php` | `/admin/tables-datatable` | `admin.tables-datatable` | `datatable()` |

Sumber: `../upcube/upcube/*.html` pada tingkat utama. HTML contoh di dalam library asset tidak dihitung sebagai halaman tugas.

## B. Enam halaman Landing

| HTML asli / view Blade | URL | Named route | Method Controller |
| --- | --- | --- | --- |
| `index.html` ? `landing/index.blade.php` | `/` | `landing.index` | `index()` |
| `about.html` ? `landing/about.blade.php` | `/about` | `landing.about` | `about()` |
| `service.html` ? `landing/service.blade.php` | `/service` | `landing.service` | `service()` |
| `menu.html` ? `landing/menu.blade.php` | `/menu` | `landing.menu` | `menu()` |
| `booking.html` ? `landing/booking.blade.php` | `/booking` | `landing.booking` | `booking()` |
| `team.html` ? `landing/team.blade.php` | `/team` | `landing.team` | `team()` |

Sumber: `../restoran/restoran-1.0.0/*.html` pada tingkat utama. Kedua paket lengkap berisi enam halaman; tidak ada halaman tugas yang dikarang atau dilewati.

## C. Dua master layout

- `resources/views/layouts/admin.blade.php`: head, header/sidebar, content, footer/settings sidebar, scripts. Login memakai kondisi sederhana sesuai struktur sumber yang tidak mempunyai header/sidebar/footer.
- `resources/views/layouts/landing.blade.php`: head, spinner, navbar, hero per halaman, content, footer, scripts.

Semua dua belas view memakai `@extends` dan section `content`; master memakai `@yield('content')`. CSS/skrip khusus Upcube tetap pada section halaman terkait dengan urutan library asli.

## D. Controller dan method

- `app/Http/Controllers/AdminController.php`: `index`, `sweetAlert`, `login`, `calendar`, `formElements`, `datatable`.
- `app/Http/Controllers/LandingController.php`: `index`, `about`, `service`, `menu`, `booking`, `team`.

Setiap method hanya me-return view yang tercantum pada tabel A/B. Tidak ada logika database atau autentikasi.

## E. Routing

Seluruh route penilaian didefinisikan di `routes/web.php`; tabel A/B memuat daftar lengkap URL, nama route dan method. Semua menggunakan `Route::get()` menuju Controller, tanpa `Route::view()` atau closure halaman. Route framework bawaan untuk health/storage bukan halaman tugas; `route:list --except-vendor` menampilkan tepat 12 route aplikasi.

## F. Hasil pengujian yang dijalankan

| Pemeriksaan | Hasil aktual |
| --- | --- |
| `php artisan route:list --except-vendor` | Berhasil; 12 route aplikasi menuju dua Controller |
| `php artisan view:cache` | Berhasil, seluruh view Blade terkompilasi |
| `php artisan optimize:clear` | Berhasil, termasuk cache berbasis file tanpa database |
| PHP lint kedua Controller dan `routes/web.php` | Tidak ada kesalahan sintaks |
| PHPUnit (`php vendor/phpunit/phpunit/phpunit --configuration phpunit.xml`) | 14 tes, 74 assertion, seluruhnya lulus; termasuk 12 kasus halaman dan 2 tes bawaan Laravel |
| HTTP 12 halaman dengan server `artisan serve` | Seluruhnya HTTP 200 |
| Perbandingan hasil HTML vs sumber | 12/12 cocok berdasarkan token HTML: tag, atribut dan teks; URL disesuaikan serta whitespace dinormalisasi |
| Hash sumber | 1.349 file sumber diperiksa; 0 perubahan |
| Salinan asset vs sumber | 0 perbedaan byte, termasuk CSS, JS, font, gambar dan ikon yang tersedia |
| HTTP asset yang dirujuk HTML/CSS | 139 URL diperiksa: 138 HTTP 200, 1 HTTP 404 (favicon Restoran yang tidak tersedia dari sumber) |
| Referensi CSS lokal | 1 file font tidak ditemukan dari sumber; detail di bagian H |
| `composer validate --no-check-publish` | Valid |
| Perbandingan visual lewat browser | Belum dilakukan: peluncuran Edge ditolak peninjauan persetujuan otomatis karena memerlukan izin sandbox yang tidak tersedia |

Perintah dijalankan dari root workspace dengan path `uts-blade/artisan` dan konfigurasi PHPUnit proyek. Percobaan awal menjalankan PHP dengan working directory langsung di folder proyek menemui izin tulis lingkungan sandbox; menjalankannya dari root workspace berhasil. Ini bukan perubahan pada aplikasi. Unduhan jaringan Composer tidak tersedia; skeleton Laravel baru dan dependensi berhasil dipasang dari cache Composer lokal, dengan lock file proyek yang valid. Tidak ada package tambahan di luar skeleton standar.

Kesetaraan HTML dan hash asset bukan bukti kesetaraan piksel. Pengujian HTTP tidak menjalankan JavaScript di browser dan tidak memverifikasi akses CDN eksternal.

## G. Perubahan terhadap hasil konversi

- Memindahkan dokumen bersama ke dua master Blade dan isi asli ke 12 view individu.
- Menggunakan section untuk judul, hero, library khusus, dan bentuk body login sesuai sumber.
- Mengganti URL link/form ke 12 halaman yang tersedia menjadi named route, serta path asset lokal menjadi helper `asset()`.
- Menyalin asset dengan struktur direktori internal yang sama. Isi CSS, JavaScript, gambar, font dan favicon yang tersedia tidak diubah.
- Menambahkan dua Controller, 12 route, dokumentasi dan pemeriksaan integrasi.
- Mengatur session/cache ke file serta queue ke sync agar halaman dapat berjalan tanpa database.

Template HTML dan asset asli tidak dimodifikasi. Teks, ikon, class, inline style bawaan, CDN, struktur visual dan urutan library dipertahankan; tidak ada CSS atau JavaScript visual tambahan.

## H. Keterbatasan dan kekurangan bawaan sumber

1. Restoran merujuk `img/favicon.ico`, tetapi file ini tidak tersedia dalam sumber. Referensi Blade dipertahankan sebagai `asset('assets/landing/img/favicon.ico')`; tidak dibuat favicon pengganti. Gambar `img/logo.png` juga disebut dalam komentar HTML yang tidak aktif, tetapi file tidak tersedia dan tidak dimuat browser.
2. CSS asli Upcube `assets/css/app.min.css` merujuk `../fonts/iter-bold.woff?v=3.13`, tetapi file tersebut tidak tersedia. CSS tidak diubah dan font pengganti tidak dibuat.
3. Ada 62 target HTML Admin dan 2 target HTML Landing di navigasi yang tidak diberikan dosen. Atribut link asli dipertahankan; tujuan ini tidak memiliki route/halaman tambahan dan dapat menghasilkan 404. Daftar lengkap ada di bawah.
4. Link kosong, anchor, dan JavaScript bawaan template tetap dipertahankan. Form login hanya tampilan, reservasi tidak disimpan, dan form lain tidak diberi backend tambahan.
5. Skrip asli Upcube `assets/js/app.js` masih memuat URL relatif `assets/css/...` saat memilih mode RTL atau kembali dari RTL. Karena URL halaman Laravel bertingkat, pilihan tersebut dapat meminta URL CSS yang tidak tersedia. Skrip tidak diubah sesuai batasan; perpindahan mode ini belum diuji melalui browser dan bukan persyaratan halaman utama.
6. CDN asli Restoran (font Google, ikon, jQuery, Bootstrap) tetap eksternal dan memerlukan internet. Tidak dilakukan penggantian atau klaim bahwa seluruh CDN dapat diakses di lingkungan ini.
7. Perbandingan visual, animasi, dan interaksi browser belum terverifikasi karena peluncuran browser ditolak oleh peninjauan persetujuan otomatis. Seluruh route wajib tetap berhasil dirender melalui HTTP.

### Target link Admin yang tidak disertakan

- `advance-notifications.html`
- `advance-rangeslider.html`
- `advance-rating.html`
- `advance-roundslider.html`
- `advance-session-timeout.html`
- `auth-lock-screen.html`
- `auth-recoverpw.html`
- `auth-register.html`
- `charts-apex.html`
- `charts-chartjs.html`
- `charts-flot.html`
- `charts-knob.html`
- `charts-sparkline.html`
- `email-inbox.html`
- `email-read.html`
- `form-advanced.html`
- `form-editors.html`
- `form-mask.html`
- `form-uploads.html`
- `form-validation.html`
- `form-wizard.html`
- `icons-dripicons.html`
- `icons-fontawesome.html`
- `icons-materialdesign.html`
- `icons-remix.html`
- `layouts-boxed.html`
- `layouts-colored-sidebar.html`
- `layouts-compact-sidebar.html`
- `layouts-dark-sidebar.html`
- `layouts-hori-boxed-width.html`
- `layouts-hori-colored-header.html`
- `layouts-hori-preloader.html`
- `layouts-hori-topbar-light.html`
- `layouts-horizontal.html`
- `layouts-icon-sidebar.html`
- `layouts-preloader.html`
- `maps-google.html`
- `maps-vector.html`
- `pages-404.html`
- `pages-500.html`
- `pages-directory.html`
- `pages-invoice.html`
- `pages-starter.html`
- `pages-timeline.html`
- `tables-basic.html`
- `tables-editable.html`
- `tables-responsive.html`
- `ui-alerts.html`
- `ui-buttons.html`
- `ui-cards.html`
- `ui-carousel.html`
- `ui-dropdowns.html`
- `ui-general.html`
- `ui-grid.html`
- `ui-images.html`
- `ui-lightbox.html`
- `ui-modals.html`
- `ui-offcanvas.html`
- `ui-progressbars.html`
- `ui-tabs-accordions.html`
- `ui-typography.html`
- `ui-video.html`

### Target link Landing yang tidak disertakan

- `contact.html`
- `testimonial.html`

Data terperinci: `audit.json`. Hash awal sumber: `source-sha256.json`. Audit dapat dijalankan ulang melalui `scripts/verify.py` dengan server Laravel aktif.

Catatan workspace: folder sementara `../.build` (cache Composer dan skrip konversi) serta `docs/http` (snapshot hasil render saat audit) masih tersedia. Peninjauan persetujuan otomatis menolak penghapusan rekursif folder sementara karena memerlukan izin sandbox yang tidak tersedia. Folder tersebut tidak dipakai routing atau aplikasi Laravel.
