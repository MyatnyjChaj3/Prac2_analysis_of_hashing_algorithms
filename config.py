
import os
import string

CHARSET = string.digits + string.ascii_lowercase + string.ascii_uppercase

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DICTIONARY_DIR = os.path.join(CURRENT_DIR, "dictionaries")
ROCKYOU_PATH = os.path.join(DICTIONARY_DIR, "rockyou.txt")
DICTIONARIES = [ROCKYOU_PATH]
# Целевые хэши из задания
TARGETS = {
    "SHA-1": [
        "7c4a8d09ca3762af61e59520943dc26494f8941b", 
        "d0be2dc421be4fcd0172e5afceea3970e2f3d940",
        "666846867fc5e0a46a7afc53eb8060967862f333",
        "6e157c5da4410b7e9de85f5c93026b9176e69064"
    ],
    "MD5": [
        "e10adc3949ba59abbe56e057f20f883e",
        "1f3870be274f6c49b3e31a0c6728957f",
        "77892341aa9dc66e97f5c248782b5d92",
        "686e697538050e4664636337cc3b834f"
    ],
    "bcrypt": [
        b"$2a$10$z4u9ZkvopUiiytaNX7wfGedy9Lu2ywUxwYpbsAR5YBrAuUs3YGXdi",
        b"$2a$10$26GB/T2/6aTsMkTjCgqm/.JP8SUjr32Bhfn9m9smtDiIwM4QIt2ze",
        b"$2a$10$Q9M0vLLrE4/nu/9JEMXFTewB3Yr9uMdIEZ1Sgdk1NQTjHwLN0asfi",
        b"$2a$10$yZBadi8Szw0nItV2g96P6eqctI2kbG/.mb0uD/ID9tlof0zpJLLL2"
    ],
    "Argon2": [
        "$argon2id$v=19$m=65536,t=3,p=2$c2FsdHNhbHQ$PUF5UxxoUY++mMekkQwFurL0ZsTtB7lelO23zcyZQ0c",
        "$argon2id$v=19$m=65536,t=3,p=2$c2FsdHNhbHQ$HYQwRUw9VcfkvqkUQ5ppyYPom6f/ro3ZCXYznhrYZw4",
        "$argon2id$v=19$m=65536,t=3,p=2$c2FsdHNhbHQ$9asGA7Xv3vQBz7Yyh4/Ntw0GQgOg8R6OWolOfRETrEg",
        "$argon2id$v=19$m=65536,t=3,p=2$c2FsdHNhbHQ$+smq45/czydGj0lYNdZVXF++FOXJwrkXt6VUIcEauvo"
    ]
}