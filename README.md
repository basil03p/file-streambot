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
