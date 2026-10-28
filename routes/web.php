<?php

use App\Http\Controllers\AdminController;
use App\Http\Controllers\LandingController;
use Illuminate\Support\Facades\Route;

Route::get('/admin', [AdminController::class, 'index'])->name('admin.index');
Route::get('/admin/advance-sweet-alert', [AdminController::class, 'sweetAlert'])->name('admin.advance-sweet-alert');
Route::get('/admin/auth-login', [AdminController::class, 'login'])->name('admin.auth-login');
Route::get('/admin/calendar', [AdminController::class, 'calendar'])->name('admin.calendar');
Route::get('/admin/form-elements', [AdminController::class, 'formElements'])->name('admin.form-elements');
Route::get('/admin/tables-datatable', [AdminController::class, 'datatable'])->name('admin.tables-datatable');

Route::get('/', [LandingController::class, 'index'])->name('landing.index');
Route::get('/about', [LandingController::class, 'about'])->name('landing.about');
Route::get('/service', [LandingController::class, 'service'])->name('landing.service');
Route::get('/menu', [LandingController::class, 'menu'])->name('landing.menu');
Route::get('/booking', [LandingController::class, 'booking'])->name('landing.booking');
Route::get('/team', [LandingController::class, 'team'])->name('landing.team');
