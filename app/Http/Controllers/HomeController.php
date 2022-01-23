<?php

namespace App\Http\Controllers;

use App\Http\Requests\UploadFileRequest;

class HomeController extends Controller
{
    /**
     * @param UploadFileRequest $request
     *
     * @return [type]
     */
    public function uploadFile(UploadFileRequest $request)
    {
        return redirect()->route('home')->with('status', 'Файл обработан!');
    }
}
