# MaubotGeoPlugin


## Introduction


#### 📝 Description

The maubot implementation provides users the possibility of interacting with an automated bot on a communication platform. This enables the user to leverage services in the background, without having to understand the “inner working”. One example would be the provision of information contained in the scorpio broker on demand or the proactive information sharing of the bot for certain time sensitive information. The bot shows an example implementation of a bot that interacts with the SALTED infrastructure, by querying organizations near the location posted by a user.

The SALTED project implemented a bot, based on the open source maubot framework (see: https://docs.mau.fi/maubot/index.html), that can be integrated in any platform that uses the Matrix framework as communication protocol. The communication platform supported by Matrix, which was used here, is the Element platform, since it offers the flexible scaling of the setup by implementing bridges to more common messenger services like Telegram and WhatsApp.


#### 🏆 Value Proposition

One challenge in disseminating innovations in the field of IoT is motivating potential users who are unfamiliar with the subject and have little or usually no prior knowledge in this area. Bots are widely used on websites of service providers or online-reatil-companies and are therefore already known by most people. Therefor they can be used as a tool to give access to more complicated services by wrapping them into a familiar frontend.


#### 🎯 End User Frontend

The frontend and its basic functionality is provided by the communication platform itself:

* User says hello to the bot and asks for help:

<img src="https://raw.githubusercontent.com/SALTED-Project/MaubotGeoPlugin/master/images/HelloBot.jpeg" alt="hello bot" height="300px"/>



* User posts a location in a room

<img src="https://raw.githubusercontent.com/SALTED-Project/MaubotGeoPlugin/master/images/LocationBot.jpeg" alt="hello bot" height="300px"/>


#### 📧 Contact Information

This plugin was developed by Kybeidos GmbH (contact: team@agenda-analytics.eu)


## Requirements (e.g. Matrix, Broker ...)


**Setup your matrix installation / choose an open one**

* see: https://matrix.org/try-matrix/

**Setup your maubot installation**

* use the official documentation: https://docs.mau.fi/maubot/usage/setup/index.html   


**You need make sure, that all further requirements for the bot are met, like a running scorpio broker and the publish services endpoint neded.**

1. Setup Scorpio broker
2. Setup Publish service
3. Test the needed endpoint: ``http://your-publish-ip:8003/broker/entities``
4. You can adapt the ``PluginCode/GeoBot/base-config.yaml`` and rebuild the plugin (see next steps) or use the pre-build plugin (``../GeoBot/salted.kybeidos.geobot-v1.0.1.mbp``) and adapt the config on the maubot GUI later on.



## Adding a Plugin on maubot interface


**Plugins can be added as .mbp per drag and drop on the maubot interface** 

* e.g. at http://localhost:29316/_matrix/maubot/#/new/plugin
* see: https://docs.mau.fi/maubot/usage/basic.html
* make sure to edit the config on the maubot GUI, to adapt the publish service ip


**Plugins can be added through dropping them as .mbp in the directory /data/plugins on the maubot host (before startup of maubot)**

* see: https://docs.mau.fi/maubot/usage/basic.html
* make sure to edit the config on the maubot GUI, to adapt the publish service ip

**Plugins can be individually build from code into .mbp and then added as described before.**

* Instructios on how to build a plugin can be found at: https://docs.mau.fi/maubot/usage/cli/build.html (for the build the mbc tool is needed, which is automatically availbale where you installed maubot, locally or within the docker container)
* Adapt the ``PluginCode/GeoBot/base-config.yaml```
* e.g. ``cd ./GeoBot && mbc build -o ./salted.kybeidos.geobot-v1.0.1.mbp ./``


## License

```
    MIT License

    Copyright (c) 2023 Kybeidos GmbH

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
 ```



## Acknowledgement
This work was supported by the European Commission CEF Programme by means of the project SALTED ‘‘Situation-Aware Linked heTerogeneous Enriched Data’’ under the Action Number 2020-EU-IA-0274.
