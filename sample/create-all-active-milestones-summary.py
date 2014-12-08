import sys
import codecs
from collections import OrderedDict
from pyphabricatordb import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

def create_session():
    DBSession = sessionmaker()
    return DBSession()

estimatedTimeFieldIndex = hash.digestForIndex("std:maniphest:saladbowl:estimated-hours")
def get_task_with_tag(session, phid):
    t = session.query(maniphest.Task).filter(maniphest.Task.phid == phid).first()
    if t:
        t.owner = None
        owner = get_user(session, t.ownerPHID)
        if owner:
            t.owner = owner
        t.estimatedTime = None
        for customFieldStorage in t.customFieldStorages:
            if customFieldStorage.fieldIndex == estimatedTimeFieldIndex:
                t.estimatedTime = int(customFieldStorage.fieldValue)
        t.edgeProjectPHIDs = [
            edge.dst for edge in 
            session.query(maniphest.Edge).filter(and_(maniphest.Edge.src == phid, maniphest.Edge.type == 41)).all()]
    return t

def task_project_valid_filter(tasks, projectPHID):
    return [t for t in tasks if projectPHID in t.edgeProjectPHIDs]

def get_user(session, phid):
    return session.query(user.User).filter(user.User.phid == phid).first()

def get_project(session, phid):
    return session.query(project.Project).filter(project.Project.phid == phid).first()

def get_active_column_items(session):
    activeColumns = [column
                     for column in session.query(project.ProjectColumn).filter(project.ProjectColumn.status == 0).all()
                     if get_project(session, column.projectPHID).status == "0"]
    return [(column, task_project_valid_filter([get_task_with_tag(session, position.objectPHID) for position in column.positions], column.project.phid))
            for column in activeColumns]

def dump_milestone_summary(session, file, milestone, tasks):
    file.write("**{0}**\n".format(milestone if len(milestone) > 0 else "Backlog"))

    all_tasks = [t for t in tasks if t.status in ("open", "inprogress", "inreview", "resolved")]
    open_tasks = [t for t in all_tasks if t.status == "open"]
    inprogres_tasks = [t for t in all_tasks if t.status == "inprogress"]
    inreview_tasks = [t for t in all_tasks if t.status == "inreview"]
    resolved_tasks = [t for t in all_tasks if t.status == "resolved"]

    owner_lists = sorted(set(t.owner for t in all_tasks), key=lambda u: u.realName if u else "")
    if len(owner_lists) > 0 and owner_lists[0] is None:
        owner_lists = owner_lists[1:] + [owner_lists[0]]
    project_lists = sorted(set((t.column.project) for t in all_tasks), key=lambda p: p.name)

    file.write(u"||" + u"|".join((u"[[/p/{0}/ | {1}]]".format(owner.userName, owner.realName) if owner else "-") for owner in owner_lists) + u"|*|\n")
    file.write(u"|--" * (len(owner_lists) + 2) + u"\n")
    for project in project_lists:
        project_shortname = project.name[project.name.find("_")+1:] if project.name.find("_") != -1 else project.name
        project_link = u"[[/project/board/{0}/ | {1}]]".format(project.id, project_shortname)
        row = u"|" + project_link + u"|"
        row_open_tasks = [t for t in open_tasks if t.column.project == project]
        row_inprogress_tasks = [t for t in inprogres_tasks if t.column.project == project]
        row_inreview_tasks = [t for t in inreview_tasks if t.column.project == project]
        row_resolved_tasks = [t for t in resolved_tasks if t.column.project == project]
        for owner in owner_lists:
            open_sum = sum(t.estimatedTime or 0 for t in row_open_tasks if t.owner == owner)
            inprogress_sum = sum(t.estimatedTime or 0 for t in row_inprogress_tasks if t.owner == owner)
            inreview_sum = sum(t.estimatedTime or 0 for t in row_inreview_tasks if t.owner == owner)
            resolved_sum = sum(t.estimatedTime or 0 for t in row_resolved_tasks if t.owner == owner)

            if open_sum > 0 or inprogress_sum > 0 or inreview_sum > 0 or resolved_sum > 0:
                row = row + u"{0}, {1}, {2}, {3}|".format(open_sum, inprogress_sum, inreview_sum, resolved_sum)
            else:
                row = row + u"|"

        row = row + u"{0}, {1}, {2}, {3}|".format(sum(t.estimatedTime or 0 for t in row_open_tasks),
                                                  sum(t.estimatedTime or 0 for t in row_inprogress_tasks),
                                                  sum(t.estimatedTime or 0 for t in row_inreview_tasks),
                                                  sum(t.estimatedTime or 0 for t in row_resolved_tasks))
        file.write(row + u"\n")

    row = u"|*|"
    for owner in owner_lists:
        owner_open_tasks = [t for t in open_tasks if t.owner == owner]
        owner_inprogress_tasks = [t for t in inprogres_tasks if t.owner == owner]
        owner_inreview_tasks = [t for t in inreview_tasks if t.owner == owner]
        owner_resolved_tasks = [t for t in resolved_tasks if t.owner == owner]
        row = row + u"{0}, {1}, {2}, {3}|".format(sum(t.estimatedTime or 0 for t in owner_open_tasks),
                                                  sum(t.estimatedTime or 0 for t in owner_inprogress_tasks),
                                                  sum(t.estimatedTime or 0 for t in owner_inreview_tasks),
                                                  sum(t.estimatedTime or 0 for t in owner_resolved_tasks))
    row = row + u"{0}, {1}, {2}, {3}|".format(sum(t.estimatedTime or 0 for t in open_tasks),
                                              sum(t.estimatedTime or 0 for t in inprogres_tasks),
                                              sum(t.estimatedTime or 0 for t in inreview_tasks),
                                              sum(t.estimatedTime or 0 for t in resolved_tasks))
    file.write(row + u"\n")
    file.write(u"\n")

def dump_all_active_milestones_summary(session, file):
    milestones = dict()
    milestones_order = dict()
    for column_item in get_active_column_items(session):
        milestones.setdefault(column_item[0].name, []).append(column_item)
        milestones_order.setdefault(column_item[0].name, column_item[0].sequence)
        milestones_order[column_item[0].name] = max(milestones_order[column_item[0].name], column_item[0].sequence)
    for milestone, _ in sorted(milestones_order.iteritems(), key=lambda x: x[1]):
        if len(milestone) == 0: continue
        tasks = []
        for column_item in milestones[milestone]:
            for t in column_item[1]:
                t.column = column_item[0]
                tasks.append(t)
        dump_milestone_summary(session, file, milestone, tasks)

def main():
    db_url = sys.argv[1] if len(sys.argv) >= 2 else 'mysql://localhost'
    file = codecs.open(sys.argv[2], "wb", "utf-8") if len(sys.argv) >= 3 else sys.stdout
    connector.connect_all(db_url)
    session = create_session()
    dump_all_active_milestones_summary(session, file)

if __name__ == "__main__":
    main()
