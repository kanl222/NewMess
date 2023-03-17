BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Session" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_user"	INTEGER NOT NULL UNIQUE,
	"key_session"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_user") REFERENCES "Users"("id")
);
CREATE TABLE IF NOT EXISTS "Users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	INTEGER NOT NULL UNIQUE,
	"password"	INTEGER NOT NULL UNIQUE,
	"icon"	TEXT NOT NULL,
	"salt"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Messages" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"message"	TEXT NOT NULL,
	"datetime_"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "Users"("id"),
	FOREIGN KEY("chat_id") REFERENCES "Chat"("id")
);
CREATE TABLE IF NOT EXISTS "Chat" (
	"id"	INTEGER NOT NULL UNIQUE,
	"title"	TEXT NOT NULL UNIQUE,
	"icon"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "СhatParticipant" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_chat"	INTEGER NOT NULL,
	"id_user"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_chat") REFERENCES "Chat"("id"),
	FOREIGN KEY("id_user") REFERENCES "Users"("id")
);
INSERT INTO "Users" VALUES (1,'BaseDate','1dfs@gmail.com','e726ae232c64ce34638629a3031c2ded6244a19a24d95bf47dae2c0b88e246c7','iVBORw0KGgoAAAANSUhEUgAAAC0AAAAtCAYAAAA6GuKaAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFaUlEQVRYhd2ZXWyTVRiAn/e0Xbd2Dt2IExDBbbCAcIEbMfGX+BcMECMZFxOHCNs0GtSgRqMh6qVi1HixwBwdrs5fjCxeYdREjQqI8w81lY1hFGSMjf2wrRvteb0AltK13daWKT53fc/53vPkfF/Pr2yuaPA+4V/TD7C66LWcxpYNfSDKOJlWXT7Va71LEF2IUCRQqIgnokoX6GGU/Rb7rRkY3tvS2Ng73vyxkGQeurKyMt8hdrWIuQdYALjG+6xCENXdgL/H5X6vo6bm5ETbn5B0wf1r5xjr2CTISgTvRBuLRpVuQes0ZF9sqa/vGO9z45LOr6jwZme5nzSqGxFJWTYahWMKm1ox9dTWnhqr/pjSRVX3XoU43xFkQXoUE6B8YoNDq1v9/mOJqiWULqqsLBPR7eejdxNwWC1lLXV1u+NViCs9p3r93Yr4Bcz5cYuPwoDV0JKDr2//NlZ5TOmCqvtuNeJoEvDEKp8UVI+Ewnpzm88XiC4aJX3lunXFDqfZIzBlcuwSoYHBMNf+tW1bV2T0nFefX1HhdThlx39DGECKMx3UR0fPkc7Jcj87KaPERFBWFFauWxMZGvk8Cqqq5jpEfwGcky42BgrH+gaHCtr9/n6I6Gkj9iX+g8IAApdelOV+OuL36T+f0yE/IZIx0YRedybT83JHxcPWMhwK0T8YpHugH9Vxr8FioujRHqd7TkdNzUkngHGYRxEmLAxwTfFctjy0IXZDqoSs5Vh3N027v+H1j3fRHwwmJS3IZVNODa3pgBpDdbXLCHcmlSkKq4q1FmvtSM86jWFGXh4PLluOf+PjZGUk1TdnWQXgLCB0DZhpaXCmfPMLfN/aCoCI4M3MZP7MmTx210oWFRSyYNYsVl1/Aw2ffZpUfhG5blp1+VRjVG5Lh3A0qsrJwUH2/v47j2zdSthaAEqKilJJ6/Ja7xIjSGlaLBNwtPvEyLfscjhSSyZaahAtTINXQrIzs/C43QDs/+OPFLNJoQEpTl0rPkaE6qVLcRjD8d5e3v3yy9QSCsVpnUzuKCll4azZADiMYYrHw/Xzr2Lh7Nkc6eri4dotdPaltKcF0jwDrr3l1rhlX/yyn87e1IUhzdJ7AgG6+09vro0I7owMLs+byuz8fMpvvInlixezYesWvv7tt5TaSav0y00fjozTZxGgpGgOL62vZHpuLq9UVnP7pmfoGRhIuh0DOmpnkE4U2NdygOfeagTgkuxslpakMMoqAYPqobTYjcGPbQcJhcMAzJ0xI+k8LqsdxkPOoTR5JcRaiz2zHjGS1MEWABdnDQVMn/S+mS6xRMybOXNkNmxrb082zalDw+FGcxDnHuDvdMnFYnpuHs+Wr0ZECA4Ps6v5u6TyqOpXf9e+fdxJbe0pW1XZZIQHUpVbVFBITpYHESHD6SQ3O5t5V1zBstLF5Hg8qCovN+2kvbs72SbehzNDng3bV41D1iWzc4nkqbJVcctOBoNs/mAHb3/xeVK5FT3a43I3wBnpNp8vUFS9fpfAiokmGxwe5s/jx0c3opb+4BBHujrZd+AAO3d/Q2dfX1LCpxHf2WPhC3I3PrK4PdHc3JlXcvVFwHX/ml0M9DQP/bn9jX1nY+cc1vQODj2v6P7JV0uA8FFrna8hMnSOdLvf3x8OaZlCz+SaxUMDwTD3RUdHHeO2+XwBq+EyheRXNOlA9UgopHdGHz5CxDcdyYnmHw7mlSw6pMhdkuRlUiooDFjCS9u21f8UqzzuLrPru+9/zl109a+CLkt1/J4gh7Esb63z7Y1X4YK8cxlzP9/V/GOHa/6CBpfLGRbV0vPR62dutza2iHniRH39mDPQ//ceMZoL6sY2Fv/G3fg/LpoxAQGYYKcAAAAASUVORK5CYII=',NULL);
INSERT INTO "Users" VALUES (2,'Join','sada@gmail.com','6d380820671a3155c904bfcf213be62524c6c2f867455dbfcc15013e0d5fd437','iVBORw0KGgoAAAANSUhEUgAAAC0AAAAtCAYAAAA6GuKaAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEhUlEQVRYhe2ZbYhUVRjHf8+9c3dtd8NXtjXQD77sIhm9sGAvYDvTLmtCGLEWZAhJtbUrEqEEgYQEfUjBPthiFBlKISmR9CEWh1klClc3P6QG27KikKZT6drOzs7MnXufPuiM6zgvOzN31jX6wXy455z7P3/O3HvP8zxHwi1r6+qPHIhQIjv6+ubVOU5LIuk+4sbthxJmvFEMakzTStjxxAzTMsJgnK8eq/l1xPr9xE/ng8cXnF55Zf7812PbtolbSP/LmT/MtjZ8E3th587xVJuUYvTTYPA+2zDWicjLqC4HrCJujwHHgH2uyNfdfn/RC1aU6d1Hjy5Vx9kq8LxCbbGTZaIwgupnScv6cNPKlX9O9r5Jmd7e21tbZ1nvKLwtHpjNQlhhqzk0tKezs9MuNLig6V2h0AMm7AeWe2IvDwpBse11b7a3h/ONy2t6d19fh6v6RYVWNxcX1HE6utrajuUakNN0Tyj0ksA+wKiItXyoRl3Vlu7W1hPZurOa7jl8uFUM4xAiNZV1lxtVvYhIoCsQGMzsu810TyjUJNAPzJwSd/kZtBKJJ15dterKxMZb/vrtvb21AgeZHoYBmuyqqj2ZjbeYvtey3mMKvhJF8uzHodD6iQ3px2NXMNhoGsYZwDfltgoTjtj2oi3t7WMwYaUNkR1MT8MA9XWW9W7qQiD98v0CVJWjXO3zUVNdnbXvWjSKq1qO/CVXZGm33x+5vrKqbyFSlmGARfX1PNXUlLVvf38/I9FoOfINpup6oMf4ZGDAEpE15ailSCSTjESj6V80HvdCNo3CWgBf8urVFYZpzvdCdDgcZjh8M2xoamjAv2yZF9IpntzR1zfPENNs81K1wlh1jtNiCDTfaSdFYZrNBrD4TvsoBnXdxQaQ/XWfvjRNfdjpAf+bniruWtO3ZQbTnEEDGL7TLopBDGPYUBio2ARSUgErP44zYKjjHPZe+TozrJvVsqRbsGw3GeyIaR4xfLNn9wN/eKGYyf2zZgHXoz+PIr4fN/v9fxmdzc22qh4qR+nhhQtZOHcu91RVUWWazKqp4fElS1gwZw4AQ5cvl5sAACBwAFLplchHwAZKzFwaGxqYU1uL3jA28Vn+OxLh+NmzZdoF4JIjshdufKe7AoFBVe0tVW10fBw7mUREEBFUldFYjJ/PnePbkyeJJ5NemP48VRZOJ7Ku6mZT5BlKSG6/P3UKUwTL58MyTWzHIW7blP9ApAlHbPuD1EV6R9zY2vqbwM5SVR1VYrbNaCxGzFvD6sKWVPkAMrbxUdveBpz2bj5P+K47ENg7seEW01va28cUOoBrU2orN4NWIvFKZuNtAVNXIDCojtOBaln5frmo6kWFNZnFR8gR5XW1tQVV5DXAk22saFSjqvpctjIv5AlNuwKBr0TkRYWxXGMqxAV13adzFdShQDz9ht9/0IUVTNHLqRDEth/Nd3QBk0gCNgYCZyK2/RjwfgVXPazQaQ4NrS50SAT/5XPETO6qE9tspM7GXcN4EFgCLBbVmwdMIlcULgCnETmRHB8/vmn16n/KmfNf+z299R6WqnAAAAAASUVORK5CYII=',NULL);
INSERT INTO "Users" VALUES (3,'kanl222','kanl222@gmail.com','a87cb3823132eb54b3959f90371ea6aaf5f0f9107305020f3e0642b7a4746133','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',NULL);
INSERT INTO "Users" VALUES (4,'Join222','Join222@gmail.com','30bf7ac22bc6a9da6d8eaa19fb0ef65f0c5c76fbd7c397eecda469714578976f','iVBORw0KGgoAAAANSUhEUgAAAC0AAAAtCAYAAAA6GuKaAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEX0lEQVRYhe2ZX4hUVRjAf9+ZOzvpppZpGomC/5ZIJUQwC8LKiAQxch1FZaGo1laRCJdA2l3GpR5SqgdZdksyVhBdt4elF6WFDCr8Rw+hxkb7Ylq2tjY2u+PuzJ3z9eDMujvOzDpzZ2c1+sHA3HPP/c6Pc+8995zvSMOL+6deHfwo1nTiQh8FcKilYZqjzkpjdTEi8xHmKUwcqqBcE7iswjmxnBlw3dNbdoT+KaStFFLIRR2fvT8jntDNwBaFRQL+PC4fUNWTgjlobawtuC2Ud2flJd3e3LgAlToMr6CU59tYBsJq2a+u+TC4Y9fVO73ojqRb9+wsL5885V2r8o5QFNl0eoC6Xrl4oLr60/holUeVbt+3+3EccxhYVAy7nCidUeKbq94K9eSqllP6y+bGSkW+YGx6NxuXXUvlxpr3TmarkFW6rWn3JmPMQcCMiVpuopKwK9dtqz+T6WRG6SNNjat8RjoYPnSVGFX9XZXngjV1XennbpNua2qsMEZOAVNKYpcDVe1Sv/tU8PXQteHlI259656d5cZIO3eBMICIVEii7EB6+QjpiZOmNFCKUSIPRHXN0ebdVSPKUn8O72tY6Dj+84BTcrPR6YlGAnOramv7YVhPO45/L3enMMDD5fcP7kodCAy9fD8BZV4i+wP3MWHipIzn+q5fw9qEl/BXbCK+ILgt1OcAGCNv41EYYNbcx1j6zOqM544faaYv3Osl/Ezx+auAJtPS8qYfWOslWop4bJBIuHfoNxAtaLabHdX1AM6D7uzl+HikGDEvdV/gUveFoeM5C5ew7Nk1xQh9E5GnD7U0TDPGZ18oXtSxRcDvqLPSgFk23jL5YGCZUdV54y2SDwrzjIhUjLdInlSMx7TTM/9Ll4p7U1pVb1sZ3OV0GRHpHm+LfBDoNmDPjlkDpvhPn4WzxibM10WPnKQsMOFWY67rOZ5C3BX3hPnbuXgK+MNzxAxMf3QOcHP2dyMa8R5Q9ftN1aG/TDIN1eEl1sInVjBz9nwCE8pxygJMeuAhlqxYxYxZcwH47dfzqLXepUWOQnJ5Za1+Yoy8RoELgTkLFjN56nRUFVBEbj3L4d4/OXf6G+/CcEUT8VZIjtPJhMjxQqP1R8K48RgigohBVemPhPn5x+/4tqOV+OCAZ2NRPk+lhYcWsq4b3+k4/pcoYHH7w7E2jM+H3x/A5y/DjceIDd4AVc+ySXr6+wIfpA6G7uPG7aFfQD8uNKpNJBgciBKNhIkNRIsprIqtTaUPIO0zHo1cDwHnitVaMVCRr9ZvrW8dXjZCuqp2b7+1WglcL6lZFlS1S32xV9PLb/tkBWvquhI3xaMlMctCMmu6Nj35CFlmeRtq6jqttW8ARRhcCyJqrL6cKc0LOaamwZr6Q4JuAPqz1RkjLruW57Ml1GGU+fS6rXXtuHY5pXo5lc6oxpfm2rqAO1gEVG6vPx+NhJ8U0UYdu17vAap7zcXVo20SwX95HzGde2rHNhPjsTf+Lz17yr7InCPCAAAAAElFTkSuQmCC',NULL);
COMMIT;