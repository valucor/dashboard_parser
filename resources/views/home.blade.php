<x-app-layout>
    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white overflow-hidden shadow-xl sm:rounded-lg">
                <div class="max-w-xs ml-10 my-5 bg-white rounded-lg border border-black-200 overflow-hidden md:max-w-xs">
                    @if (session('status'))
                        <div x-data="{ show: true }" x-show="show" x-init="setTimeout(() => show = false, 3000)"
                        class=" my-3 text-sm text-left text-green-600 bg-green-500 bg-opacity-10 border border-green-400 h-12 flex items-center p-4 rounded-md"
                        role="alert"
                        >
                        {{ session('status') }}
                        </div>
                    @endif
                    @error('file')
                        <div x-data="{ show: true }" x-show="show" x-init="setTimeout(() => show = false, 3000)"
                        class=" my-3 text-sm text-left text-red-600 bg-red-500 bg-opacity-10 border border-red-400 h-12 flex items-center p-4 rounded-md"
                        role="alert"
                        >
                        {{ $message }}
                        </div>
                    @enderror
                    <form method="post" action="{{ route('upload_file') }}">
                        @csrf
                        <div class="md:flex">
                            <div class="w-full">
                                {{-- <div class="p-4 border-b-2"> <span class="text-lg font-bold text-gray-600">Upload file</span> </div> --}}
                                <div class="flex justify-center p-3 border-b-2">
                                    <div class="mb-2">
                                        <div class=" bg-grey-lighter">
                                            <label class="w-48 flex flex-col items-center px-0 py-3 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase border border-blue cursor-pointer hover:bg-blue-500 hover:text-white">
                                                <svg class="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                                    <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
                                                </svg>
                                                <span class="mt-2 text-base leading-normal">{{ __('Select a file') }}</span>
                                                <input type='file' name="file" class="hidden" />
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="p-3" x-data="{ show: false }">
                                    <button type="submit" @click=" show = true " class="w-full h-12 text-lg bg-blue-600 rounded text-white hover:bg-blue-700">
                                        <span x-show="!show">{{ __('Submit') }}</span>
                                        <div x-show="show" class=" flex justify-center items-center">
                                            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-white-500"></div>
                                        </div>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
