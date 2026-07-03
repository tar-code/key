**Вставьте эти строки на Colab**

<code>from google.colab import userdata
secret = userdata.get('secretName')
!git clone https://github.com/tar-code/key.git && cd key && python3 hidecode.py "{secret}"</code>
