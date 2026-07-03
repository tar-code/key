**Вставьте эти строки в блокнот Colab: https://colab.research.google.com**

<pre><code>from google.colab import userdata
secret = userdata.get('secretName')
!git clone -q https://github.com/tar-code/key.git 2>&1 >/dev/null
!python3 key/hidecode.py "{secret}"</code></pre>
