#!/usr/bin/env python3
import sys
import hashlib


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid number of arguments")
        print("Usage: integrity.py path_to_file path_to_dir ")
        sys.exit()
    else:
        path_to_file = sys.argv[1]
        path_to_dir = sys.argv[2]
        if path_to_dir[-1] != '/':
            path_to_dir += '/'

        try:
            with open(path_to_file, 'r') as f:
                for line in f:
                    if len(line.split()) == 3:
                        filename = line.strip().split()[0]
                        algorithm = line.strip().split()[1]
                        hash = line.strip().split()[2]

                        BUF_SIZE = 65536
                        md5 = hashlib.md5()
                        sha1 = hashlib.sha1()
                        sha256 = hashlib.sha256()
                        hash_sum = ''

                        try:
                            with open(path_to_dir + filename, 'rb') as f2:
                                while True:
                                    data = f2.read(BUF_SIZE)
                                    if not data:
                                        break
                                    md5.update(data)
                                    sha1.update(data)
                                    sha256.update(data)

                            if algorithm == 'md5':
                                hash_sum = md5.hexdigest()
                            elif algorithm == 'sha1':
                                hash_sum = sha1.hexdigest()
                            elif algorithm == 'sha256':
                                hash_sum = sha256.hexdigest()
                            else:
                                print(filename, "WRONG HASHING ALGORITHM")

                            if hash == hash_sum:
                                print(filename, "OK")
                            else:
                                print(filename, "FAIL")

                        except FileNotFoundError as e:
                            print(filename, "NOT FOUND")
                    else:
                        print(filename, "WRONG INPUT FORMAT")
        except FileNotFoundError as e:
            print(e)
            sys.exit()
