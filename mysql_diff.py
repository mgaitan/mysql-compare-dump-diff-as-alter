#!/usr/bin/env python

import argparse
import os
import sys
import parse

__version = "0.1.0"


def same_params(params1, params2):
    list1 = params1.split()
    list2 = params2.split()
    if len(list2) == len(list1):
        for idx, val in enumerate(list1):
            if list2[idx] != val:
                return False
    else:
        return False
    return True


def compare_two_dicts_and_return_alter(db_dict1, db_dict2):
    output_sql = ""
    for key, value in db_dict1.items():
        if key not in db_dict2:
            # no such table.
            # form create table total
            output_temp = ""
            for key2, value2 in value.items():
                output_temp = "%s\n `%s` %s," % (output_temp, key2, value2)
            output_sql = (
                "%s\n CREATE TABLE `%s` ( %s ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
                % (output_sql, key, output_temp)
            )
        else:
            # such table exists
            output_temp = ""
            for key2, value2 in value.items():
                if key2 not in db_dict2[key]:
                    # add
                    # ALTER TABLE `tablename` ADD `fieldname` [params];
                    output_temp = "%s\n ALTER TABLE `%s` ADD `%s` %s;" % (
                        output_temp,
                        key,
                        key2,
                        value2,
                    )
                else:
                    # compare params and modify if needed
                    # ALTER TABLE `tablename` MODIFY `fieldname` [params];
                    if not same_params(value2, db_dict2[key][key2]):
                        output_temp = "%s\n ALTER TABLE `%s` MODIFY `%s` %s;" % (
                            output_temp,
                            key,
                            key2,
                            value2,
                        )
            output_sql = "%s %s" % (output_sql, output_temp)
    return output_sql


def parse_db_to_dict(db_string=""):
    temp_dict = {}
    for table in parse.findall("CREATE TABLE `{}` ({}) ENGINE=InnoDB", db_string):
        # table[0] = tablename
        # table[1] = all table fields
        temp_table_dict = {}
        for field in parse.findall("`{}` {},\n", table[1]):
            # field[0] = field name
            # field[1] = field description
            temp_table_dict[field[0]] = field[1]
        temp_dict[table[0]] = temp_table_dict
    return temp_dict


def main():
    parser = argparse.ArgumentParser(
        description="Find diff in two MySQL dumps and create diff file with ALTER commands(like migration"
    )
    parser.add_argument("db_origin", type=argparse.FileType('r'), help="The origin schema")
    parser.add_argument("db_target", type=argparse.FileType('r'), help="The target schema")

    parser.add_argument("output_file", nargs="?", type=argparse.FileType('w'), default=sys.stdout, help="output file")
    args = parser.parse_args()
    
    origin = parse_db_to_dict(args.db_origin.read())
    target = parse_db_to_dict(args.db_target.read())

    diff_sql_alter = compare_two_dicts_and_return_alter(target, origin)
    print(diff_sql_alter, file=args.output_file)
