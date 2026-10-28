<?php

namespace Tests\Feature;

use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

class PagesTest extends TestCase
{
    #[DataProvider('pages')]
    public function test_page_renders_the_expected_view(string $url, string $view, string $asset): void
    {
        $this->get($url)
            ->assertOk()
            ->assertViewIs($view)
            ->assertSee('<html lang="en">', false)
            ->assertSee($asset, false)
            ->assertDontSee('@yield', false)
            ->assertDontSee('@extends', false);
    }

    public static function pages(): array
    {
        return [
            'dashboard' => ['/admin', 'admin.index', '/assets/admin/css/app.min.css'],
            'sweet alert' => ['/admin/advance-sweet-alert', 'admin.advance-sweet-alert', '/assets/admin/css/app.min.css'],
            'login' => ['/admin/auth-login', 'admin.auth-login', '/assets/admin/css/app.min.css'],
            'calendar' => ['/admin/calendar', 'admin.calendar', '/assets/admin/css/app.min.css'],
            'form elements' => ['/admin/form-elements', 'admin.form-elements', '/assets/admin/css/app.min.css'],
            'datatable' => ['/admin/tables-datatable', 'admin.tables-datatable', '/assets/admin/css/app.min.css'],
            'home' => ['/', 'landing.index', '/assets/landing/css/style.css'],
            'about' => ['/about', 'landing.about', '/assets/landing/css/style.css'],
            'service' => ['/service', 'landing.service', '/assets/landing/css/style.css'],
            'menu' => ['/menu', 'landing.menu', '/assets/landing/css/style.css'],
            'booking' => ['/booking', 'landing.booking', '/assets/landing/css/style.css'],
            'team' => ['/team', 'landing.team', '/assets/landing/css/style.css'],
        ];
    }
}
