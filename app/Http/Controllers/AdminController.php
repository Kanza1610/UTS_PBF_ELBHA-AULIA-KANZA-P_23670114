<?php

namespace App\Http\Controllers;

class AdminController extends Controller
{
    public function index()
    {
        return view('admin.index');
    }

    public function sweetAlert()
    {
        return view('admin.advance-sweet-alert');
    }

    public function login()
    {
        return view('admin.auth-login');
    }

    public function calendar()
    {
        return view('admin.calendar');
    }

    public function formElements()
    {
        return view('admin.form-elements');
    }

    public function datatable()
    {
        return view('admin.tables-datatable');
    }
}
