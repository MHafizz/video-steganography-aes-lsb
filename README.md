# Video Steganography using LSB + AES  
### Final Thesis Project – Informatics Undergraduate Program  

## Overview
This project was developed as part of my undergraduate final thesis in Informatics.  
It implements video steganography using the Least Significant Bit (LSB) method combined with AES encryption to enhance data confidentiality before embedding.

## Research Background
Traditional LSB-based steganography provides data hiding capability but lacks strong confidentiality protection.  
To improve security, AES encryption is applied to the plaintext before embedding into video frames.

## Methodology
1. Plaintext message is encrypted using AES.
2. Encrypted data is embedded into video frames using LSB technique.
4. Extraction process retrieves embedded data and decrypts it.

## Features
- AES encryption before embedding
- LSB-based video frame embedding
- Data extraction and decryption

## Technologies Used
- Python
- OpenCV
- AES Cryptography Library

## Academic Context
This research was conducted as part of the undergraduate thesis requirement in the Informatics Program.
