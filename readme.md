<center><h2>🚀 LLM-ArxivPaper: Gather Arxiv papers, enhance reading via LLMs</h2></center>

## 🎉 News
- [X] [2025.05.19]🎯📢LLM-ArxivPaper now supports displaying scraped Arxiv papers via Web UI.
- [X] [2025.05.18]🎯📢LLM-ArxivPaper now supports automated Arxiv paper scraping via Web UI.

## Installation
### Install Dependencies
```shell
git clone https://github.com/gxlover0625/LLM-ArxivPaper.git
cd LLM-ArxivPaper
pip install -r requirements.txt
```
### Install Chrome
Since LLM-ArxivPaper requires the use of Chrome for web crawling, it is necessary to install Chrome on the Linux system. The ways to install Chrome vary across different systems. Here, we demonstrate the installation method for `Ubuntu systems` without using sudo privileges.
```shell
mkdir -p ~/software/chrome  # replace the path you want to install
cd ~/software
wget https://dl.google.com/linux/google-chrome-stable_current_amd64.deb
dpkg-deb -x google-chrome-stable_current_amd64.deb ~/software/chrome
```
Now, you can find chrome in the `~/software/chrome/opt/google/chrome/chrome`. Next, create a `.env` file in the LLM-ArxivPaper directory and add the following environment variables to the `.env` file.
```
chrome_bin=~/software/chrome/opt/google/chrome/chrome
```

## Quick Start
> [!IMPORTANT]
> Please make sure to install chrome correctly.
