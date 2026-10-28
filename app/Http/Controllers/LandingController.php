<?php

namespace App\Http\Controllers;

class LandingController extends Controller
{
    public function index()
    {
        return view('landing.index');
    }

    public function about()
    {
        return view('landing.about');
    }

    public function service()
    {
        return view('landing.service');
    }

    public function menu()
    {
        return view('landing.menu');
    }

    public function booking()
    {
        return view('landing.booking');
    }

    public function team()
    {
        return view('landing.team');
    }
}
