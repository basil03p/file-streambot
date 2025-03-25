<h1 align="center">FileStreamBot (Modified)</h1>
<p align="center">
  <a href="https://github.com/basil03p/FileStreamBot">
  </a>
</p>  
  <p align="center">
    <b>
      <a href="https://github.com/basil03p/FileStreamBot/issues">Report a Bug</a>
      |
      <a href="https://github.com/basil03p/FileStreamBot/issues">Request Feature</a>
    </b>
  </p>

---

### 🍁 About :

<p align="center">
    <a href="https://github.com/basil03p/FileStreamBot">
        <img src="https://i.ibb.co/ZJzJ9Hq/link-3x.png" height="100" width="100" alt="FileStreamBot Logo">
    </a>
</p>
<p align='center'>
  This is a modified version of the original FileStreamBot. It provides stream links for Telegram files without waiting for downloads to complete, while also offering file storage capabilities.
  [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=filestreambot&repository=basil03p%2FFileStreamBot&branch=main&instance_type=free&instances_min=0&autoscaling_sleep_idle_delay=300&env%5BAPI_HASH%5D=0dd5dfd68f8df13f000beb308d43f155&env%5BAPI_ID%5D=28403078&env%5BBOT_TOKEN%5D=7271534517%3AAAELTkV_Cea_6ekfYHlgJHfMTMOkjlp-X3k&env%5BBOT_WORKERS%5D=10&env%5BDATABASE_URL%5D=mongodb%2Bsrv%3A%2F%2Fadmin%3Abasilser10%40apptest.98to3.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3Dapptest&env%5BFILE_PIC%5D=https%3A%2F%2Fimghost.net%2Fib%2FmpWBXm91Q2pvtm4_1742709593.jpg&env%5BFLOG_CHANNEL%5D=-1002531606586&env%5BFORCE_SUB%5D=True&env%5BFORCE_SUB_ID%5D=-1002036635078&env%5BFQDN%5D=basilser.koyeb.app&env%5BNO_PORT%5D=True&env%5BOWNER_ID%5D=1611849472&env%5BSTART_PIC%5D=https%3A%2F%2Fimghost.net%2Fib%2FmTyJAPnWQyw2ri3_1742709472.jpg&env%5BULOG_CHANNEL%5D=-1002531606586&env%5BVERIFY_PIC%5D=https%3A%2F%2Fimghost.net%2Fib%2FWovFgQ5FYWjuzru_1742709690.jpg)
</p>

---

### ♢ How to Deploy :

<i>You can deploy on Koyeb, locally, or on a VPS.</i>

#### ♢ Click on This Drop-down and get more details

<details>
  <summary><b>Deploy on Koyeb (Free) :</b></summary>

- Fork this repository.
- Click on the button below to deploy easily.

  [![Deploy to Koyeb](https://deploy.koyeb.app/deploy-button.svg)](https://app.koyeb.com/deploy?type=git&repository=https://github.com/basil03p/FileStreamBot)

- Follow the instructions in Koyeb to set up your bot.
- Go to the <a href="#mandatory-vars">variables tab</a> for more info on setting up environmental variables.

</details>

<details>
  <summary><b>Deploy Locally :</b></summary>

```sh
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot
python3 -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
python3 -m FileStream
