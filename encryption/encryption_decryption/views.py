from io import BytesIO
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views import View
from .forms import DecryptionForms, EncryptionForms
import pyAesCrypt


def index(request):
    return redirect('encryption')


class EncryptionView(View):
    def get(self, request):
        title = 'Encryption'
        button_name = 'Encryption and download'
        form = EncryptionForms()
        return render(request, 'index.html', {'form': form, 'button': button_name, 'title': title})

    def post(self, request):
        title = 'Encryption'
        button_name = 'Encryption and download'
        form = EncryptionForms(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'index.html', {'form': form, 'button': button_name, 'title': title})
        encrypted_data = BytesIO()
        buffer_size = 64 * 1024
        passwd = form.cleaned_data['password1']
        file_encrypt = form.cleaned_data['file']
        pyAesCrypt.encryptStream(file_encrypt, encrypted_data, passwd, buffer_size)
        encrypted_data.getvalue()
        encrypted_file = encrypted_data.getvalue()
        response = HttpResponse(encrypted_data,  content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="encrypted_file.aes"'
        response.write(encrypted_file)

        return response


class DecryptionView(View):

    def get(self, request):
        title = 'Decryption'
        button_name = 'Decryption and download'
        form = DecryptionForms()
        return render(request, 'index.html', {'form': form, 'button': button_name, 'title': title})

    def post(self, request):
        title = 'Decryption'
        button_name = 'Decryption and download'
        form = DecryptionForms(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'index.html', {'form': form, 'button': button_name, 'title': title})
        encrypted_data = BytesIO(form.cleaned_data['file'].read())
        decrypted_data = BytesIO()
        encrypted_data_len = len(encrypted_data.getvalue())
        buffer_size = 64 * 1024
        passwd = form.cleaned_data['password']
        try:
            pyAesCrypt.decryptStream(encrypted_data, decrypted_data, passwd, buffer_size, encrypted_data_len)
        except ValueError as exp:
            form.add_error('password', exp)
            return render(request, 'index.html', {'form': form, 'button': button_name, 'title': title})
        decrypted_data.getvalue()
        encrypted_file = decrypted_data.getvalue()
        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="decrypted_file"'
        response.write(encrypted_file)

        return response



