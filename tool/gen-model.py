import sys
import os
import json
import subprocess
import codecs
import re

def generate_model(db_url, db_name, config, output_path):
    file_name = (db_name[12:] if db_name.startswith("phabricator_") else db_name) + ".py"
    src = subprocess.check_output(["sqlacodegen", db_url + "/" + db_name])

    # import required type
    mo = re.search(r"from sqlalchemy import .*", src)
    if mo:
        src = (src[:mo.end(0) + 1] + 
               "from sqlalchemy import String, Unicode, ForeignKey\n" + 
               "from sqlalchemy.orm import relationship\n" +
               "from dbdatetime import dbdatetime\n" +
               src[mo.end(0) + 1:])

    # change to unicode
    src = re.sub(r"String\(collation=u'utf\w*'\)", r"Unicode", src)
    src = re.sub(r"String\((\d+),\su'utf8\w*'\)", r"Unicode(\1)", src)
    src = re.sub(r"VARBINARY\(64\)", r"String", src)

    # change date integer to dbdatetime
    src = re.sub(r"(date\w+) = Column\(Integer,", r"\1 = Column(dbdatetime,", src)

    # change class Maniphest* to *
    src = re.sub(r"class Maniphest(\w*)\(Base\)\:", r"class \1(Base):", src)

    # change metadata to usermetadata
    src = re.sub(r"metadata = Column\(([^)]*)\)", r"usermetadata = Column('metadata', \1)", src)

    # update class and field specific
    def update_class(class_name, lines):
        config_items = [(k, v) for k, v in config.iteritems() if k.lower() == class_name.lower()]
        if len(config_items) == 0:
            return lines
        class_new_name = config_items[0][0];
        class_config = config_items[0][1];
        lines[0] = lines[0].replace(class_name, class_new_name)
        for i in xrange(1, len(lines)):
            mo = re.search(r"(\w+) = Column\((.*)\)", lines[i])
            if mo:
                field_name = mo.group(1)
                column_params = mo.group(2)
                config_items = [(k, v) for k, v in class_config.iteritems() if k.lower() == field_name.lower()]
                if len(config_items) == 0:
                    continue
                field_new_name = config_items[0][0];
                field_config = config_items[0][1];
                foreignKey = field_config.get("ForeignKey")
                if foreignKey:
                    columns = column_params.split(",");
                    column_params = ",".join(columns[0:1] + [" ForeignKey(\"" + foreignKey + "\")"] + columns[1:])
                lines[i] = "    {0} = Column({1})".format(field_new_name, column_params)
        class_code = class_config.get("__code__")
        if class_code:
            lines.append("")
            for code in class_code:
                lines.append("    " + code)
        return lines

    # update class specific
    i = 0
    cur_class = None
    lines = src.splitlines()
    while i < len(lines): 
        mo = re.search(r"class (\w*)\(Base\)", lines[i])
        if mo:
            if cur_class:
                class_lines = lines[cur_class_firstline:cur_class_lastline+1];
                i -= len(class_lines)
                update_lines = update_class(cur_class, class_lines)
                lines = lines[:cur_class_firstline] + update_lines + lines[cur_class_lastline+1:]
                i += len(update_lines)
            cur_class = mo.group(1)
            cur_class_firstline = i
        else:
            if len(lines[i].strip()) > 0:
                cur_class_lastline = i
        i += 1;
    if cur_class:
        update_lines = update_class(cur_class, lines[cur_class_firstline:cur_class_lastline+1])
        lines = lines[:cur_class_firstline] + update_lines + lines[cur_class_lastline+1:]

    with codecs.open(os.path.join(output_path, file_name), "wb", "utf-8") as f:
        f.write("\n".join(lines))

def main():
    db_url = 'mysql://localhost'
    if len(sys.argv) >= 2:
        db_url = sys.argv[1]
    output_path = './'
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]

    with codecs.open("gen-model.json", "rb", "utf-8") as f:
        db_configs = json.load(f)

    for db_name, db_config in db_configs.iteritems():
        generate_model(db_url, db_name, db_config, output_path)

if __name__ == "__main__":
    main()
