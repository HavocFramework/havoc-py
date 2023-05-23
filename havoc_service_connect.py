from havoc.service import HavocService


def main():
    havoc_service = HavocService(
        endpoint="wss://192.168.0.148:40056/test",
        password="password1234"
    )

    print( "[*] Connected to Havoc Service" )

    return


if __name__ == '__main__':
    main()
