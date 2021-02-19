import tidalapi
import sys, getopt


def main(email, passwd):
    session = tidalapi.Session()

    # session.login(email, passwd)
    session.login("env_email","env_pass")   # Todo: use .env entries
    user = tidalapi.User(session, session.user.id)
    playlists = user.playlists()
    print(playlists)

    # Todo: delete
    # track = session.get_track('529459')

    # print(track.id, track.name)
    # print(dir(track))

    # tracks = session.get_playlist_tracks("b4d29a4e-5b67-43e2-82c2-0bcfff094f80")
    # for track in tracks:
    #     print(track.id)

    # genres = session.get_genres()

    # for genre in genres:
    #     print(genre.name)


def parse_opt(argv):
    # Todo: test and use .env
    help_phrase = "test.py -e <tidal_email> -p <tidal_password>"
    email = ''
    passwd = ''
    try:
        opts, args = getopt.getopt(argv,"he:p:",["email=","pass="])
    except getopt.GetoptError:
        print(help_phrase)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_phrase)
            sys.exit()
        if opt in ("-e", "--email"):
            print(arg)
            email = arg
        if opt in ("-p", "--pass"):
            passwd = arg

    return email, passwd


if __name__ == "__main__":
    email, passwd = parse_opt(sys.argv[1:])
    main(email, passwd)

     