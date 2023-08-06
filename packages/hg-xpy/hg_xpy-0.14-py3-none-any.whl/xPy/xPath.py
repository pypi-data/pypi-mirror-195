import os


class xPath:
    @staticmethod
    def Link(src, link):
        if os.path.exists(link):
            return
        b = os.path.isdir(src)
        os.symlink(src, link, target_is_directory=b)

    @staticmethod
    def Convert2Linux(src):
        # d:/xxx ===> /mnt/d/xxx
        import re
        result = re.sub("(?im)^([a-z]):(.*)", r"/mnt/\1\2", src)
        return result


if __name__ == "__main__":
    pass
