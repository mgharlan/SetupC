import argparse
from datetime import date
import os

class SetupC:
    def __init__(self, args):
        self.destination = args.destination
        self.cpp_files = args.cpp_files
        self.header_files = args.header_files
        self.makefile = args.makefile

    def print(self):
        print(self.destination)
        print(self.cpp_files)
        print(self.header_files)
        print(self.makefile)

    def start(self):
        if os.path.exists(self.destination):
            for cpp in self.cpp_files:
                file = open(f'{self.destination}/{cpp}.cpp', 'w+')

                if cpp in self.header_files:
                    file.write(self.cpp_file_content(cpp, True))
                else:
                    file.write(self.cpp_file_content(cpp))

                file.close()

            for h in self.header_files:
                file = open(f'{self.destination}/{h}.h', 'w+')

                if h in self.cpp_files:
                    file.write(self.h_file_content(h, True))
                else:
                    file.write(self.h_file_content(h))

                file.close()

            if self.makefile:
                file = open(f'{self.destination}/Makefile', 'w+')
                file.write(self.makefile_content())
                file.close()

    @staticmethod
    def cpp_file_content(cpp, include=False):
        content = '//Mason Harlan\n'
        content = content + '//Class\n'
        content = content + '//Assignment Title\n'
        content = content + f'//{date.today().strftime("%m/%d/%Y")}\n'
        content = content + f'//{cpp}.cpp\n'
        content = content + '/*\nChanges:\n\n*/\n\n'

        content = content + f'#ifndef {cpp.upper()}_CPP\n'
        content = content + f'#define {cpp.upper()}_CPP\n\n'

        if include:
            content = content + f'#include "{cpp}.h"\n\n'

        content = content + '\n\n#endif'

        return content

    @staticmethod
    def h_file_content(h, include=False):
        content = '//Mason Harlan\n'
        content = content + '//Class\n'
        content = content + '//Assignment Title\n'
        content = content + f'//{date.today().strftime("%m/%d/%Y")}\n'
        content = content + f'//{h}.h\n'
        content = content + '/*\nChanges:\n\n*/\n\n'

        content = content + f'#ifndef {h.upper()}_H\n'
        content = content + f'#define {h.upper()}_H\n\n\n'

        if include:
            content = content + f'\n#include "{h}.cpp"\n'

        content = content + '\n#endif'

        return content

    def makefile_content(self):
        cpp_with_h = []
        cpp_without_h = []
        content = 'objects = '

        for cpp in self.cpp_files:
            content = content + '{cpp}.o '
            if cpp in self.header_files:
                cpp_with_h.append(cpp)
            else:
                cpp_without_h.append(cpp)

        content = content + '\n'
        content = content + '\nCC = g++\nCFLAGS = -Wall\n'
        content = content + '\n'

        content = content + 'all: '
        for cpp in cpp_without_h:
            content = content + f'{cpp} '
        content = content +'\n\n'

        for cpp in cpp_without_h:
            content = content + f'{cpp}: {cpp}.o\n'
            content = content + f'\t$(CC) {cpp}.o -o {cpp}\n\n'

            content = content + f'{cpp}.o: {cpp}.cpp\n'
            content = content + f'\t$(CC) $(CFLAGS) -c {cpp}.cpp\n\n'

        for cpp in cpp_with_h:
            content = content + f'{cpp}.o: {cpp}.cpp {cpp}.h\n'
            content = content + f'\t$(CC) $(CFLAGS) -c {cpp}.cpp\n\n'

        content = content + 'clean:\n\t-rm $(objects)'

        return content

def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-dst', '--destination', type=str, default='', help='provide a destination to create project in')
    parser.add_argument('-cpp', '--cpp_files', nargs='+', type=str, help='provide cpp files to create')
    parser.add_argument('-hpp', '--header_files', nargs='+', type=str, help='provide header files to create')
    parser.add_argument('-make', '--makefile', action='store_true', help='create makefile')

    return parser.parse_args()

if __name__ == "__main__":
    argv = setup_parser()
    setup = SetupC(argv)
    setup.start()