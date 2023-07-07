from redvid import Downloader


def main():

    reddit = Downloader(max_q=True, overwrite = True)
    reddit.url = 'https://www.reddit.com/r/pythonforengineers/comments/hfmo98/what_kind_of_hawk_is_this/'
    file = reddit.download()
    title, comment = reddit.get_title_comment()


    print('printing file',file)
    print(title, comment)

    # NOW WE HAVE TITLE, COMMENT AND VIDEO FILE

    # NOW WE NEED TO READ VIDEOS AND CHECK ITS RESOLUTION, I.E. MAKE IT 9:16 WITH FILLERS




if __name__=='__main__':
    main()