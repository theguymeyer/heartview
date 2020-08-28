This link has been really useful when creating a Personal Information Exchange (.pfx) file for code signing:

>> MakeCert /r /h 0 /eku "1.3.6.1.5.5.7.3.3,1.3.6.1.4.1.311.10.3.13" /e "12/31/2021" /sv hv_key.pvk hv_key.cer
>> Pvk2Pfx /pvk hv_key.pvk /spc hv_key.cer /pfx hv_key.pfx

Then apply codesigning...

>> cd ../dist
>> SignTool sign /f ../codesigning/hv_key.pfx /t http://timestamp.digicert.com HeartView.exe

If experiencing issues with comm port connectivity then you must install ST Link driver software:

Go to  https://www.st.com/en/development-tools/stsw-link009.html
.. download the zip folder and follow the README instructions