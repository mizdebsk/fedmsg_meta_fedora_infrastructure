# This file is part of fedmsg.
# Copyright (C) 2015 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Pierre-Yves Chibon <pingou@pingoured.fr>
#

from fedmsg_meta_fedora_infrastructure.fasshim import avatar_url, email2fas
from fedmsg_meta_fedora_infrastructure import BaseProcessor

import fedmsg.meta.base

class PagureProcessor(BaseProcessor):
    topic_prefix_re = 'io\\.pagure\\.(dev|stg|prod)'

    __name__ = "pagure"
    __description__ = "Pagure forge"
    __link__ = "https://pagure.io"
    __docs__ = "https://pagure.io/pagure"
    __obj__ = "Pagure forge"
    __icon__ = ("https://apps.fedoraproject.org/packages/"
                "images/icons/package_128x128.png")

    def __get_project(self, msg, key='project'):
        ''' Return the project as `foo` or `user/foo` if the project is a
        fork.
        '''
        project = msg[key]['name']
        if msg[key]['parent']:
            user = msg[key]['user']['name']
            project = '/'.join([user, project])
        return project

    def link(self, msg, **config):
        try:
            project = self.__get_project(msg['msg'])
        except KeyError:
            try:
                project = self.__get_project(msg['msg']['pullrequest'])
            except KeyError:
                project = "(unknown)"

        base_url = "https://pagure.io"

        tmpl = '{base_url}/{project}'
        if '/' in project:
            tmpl = '{base_url}/fork/{project}'
        if 'pagure.issue' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            if 'comment' in msg['topic']:
                tmpl += '/issue/{id}#comment-{comment}'
                return tmpl.format(
                    base_url=base_url, project=project, id=issueid,
                    comment=len(msg['msg']['issue']['comments']))
            else:
                tmpl += '/issue/{id}'
                return tmpl.format(
                    base_url=base_url, project=project, id=issueid)
        elif 'pagure.pull-request' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            if 'comment' in msg['topic']:
                tmpl += '/pull-request/{id}#comment-{comment}'
                return tmpl.format(
                    base_url=base_url, project=project, id=prid,
                    comment=len(msg['msg']['pullrequest']['comments']))
            else:
                tmpl += '/pull-request/{id}'
                return tmpl.format(
                    base_url=base_url, project=project, id=prid)
        elif 'pagure.project' in msg['topic']:
            return tmpl.format(base_url=base_url, project=project)
        elif 'pagure.git.receive' in msg['topic']:
            project = self.__get_project(msg['msg']['commit'], key='repo')
            commit = msg['msg']['commit']['rev']
            tmpl += '/{commit}'
            return tmpl.format(
                base_url=base_url, project=project, commit=commit)
        else:
            return base_url

        return None

    def subtitle(self, msg, **config):
        try:
            project = self.__get_project(msg['msg'])
        except KeyError:
            try:
                project = self.__get_project(msg['msg']['pullrequest'])
            except KeyError:
                project = "(unknown)"
        user = msg['msg'].get('agent')

        if 'pagure.project.new' in msg['topic']:
            tmpl = self._(
                '{user} created a new project "{project}"'
            )
            return tmpl.format(user=user, project=project)
        elif 'pagure.issue.new' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            title = msg['msg']['issue']['title']
            tmpl = self._(
                '{user} opened a new ticket {project}#{id}: "{title}"')
            return tmpl.format(
                user=user, project=project, title=title, id=issueid)
        elif 'pagure.issue.comment.added' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            title = msg['msg']['issue']['title']
            tmpl = self._(
                '{user} commented on ticket {project}#{id}: "{title}"')
            return tmpl.format(
                user=user, project=project, title=title, id=issueid)
        elif 'pagure.issue.tag.added' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            tags = msg['msg']['tags']
            tags = fedmsg.meta.base.BaseConglomerator.list_to_series(tags)
            tmpl = self._(
                '{user} tagged ticket {project}#{id}: {tags}')
            return tmpl.format(
                user=user, project=project, id=issueid, tags=tags)
        elif 'pagure.issue.tag.removed' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            tags = msg['msg']['tags']
            tags = fedmsg.meta.base.BaseConglomerator.list_to_series(tags)
            tmpl = self._(
                '{user} removed the {tags} tags from ticket {project}#{id}')
            return tmpl.format(
                user=user, project=project, id=issueid, tags=tags)
        elif 'pagure.issue.assigned.added' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            assignee = msg['msg']['issue']['assignee']['name']
            tmpl = self._(
                '{user} assigned ticket {project}#{id} to {assignee}')
            return tmpl.format(
                user=user, project=project, id=issueid, assignee=assignee)
        elif 'pagure.issue.assigned.reset' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            tmpl = self._(
                '{user} reset the assignee of ticket {project}#{id}')
            return tmpl.format(user=user, project=project, id=issueid)
        elif 'pagure.issue.dependency.added' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            dep_id = msg['msg']['added_dependency']
            tmpl = self._(
                '{user} added ticket {project}#{id} as a dependency of '
                'ticket {project}#{dep_id}'
            )
            return tmpl.format(
                user=user, project=project, id=issueid,
                dep_id=dep_id)
        elif 'pagure.issue.dependency.removed' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            removed = msg['msg']['removed_dependency']
            tmpl = self._(
                '{user} removed ticket {project}#{id} as a dependency '
                'of ticket {project}#{removed}'
            )
            return tmpl.format(
                user=user, project=project, id=issueid, removed=removed)
        elif 'pagure.issue.edit' in msg['topic']:
            issueid = msg['msg']['issue']['id']
            fields = msg['msg']['fields']
            fields = fedmsg.meta.base.BaseConglomerator.list_to_series(fields)
            tmpl = self._(
                '{user} edited the {fields} fields of ticket '
                '{project}#{id}'
            )
            return tmpl.format(
                user=user, project=project, id=issueid, fields=fields)
        elif 'pagure.project.edit' in msg['topic']:
            fields = msg['msg']['fields']
            fields = fedmsg.meta.base.BaseConglomerator.list_to_series(fields)
            tmpl = self._(
                '{user} edited the {fields} fields of project {project}')
            return tmpl.format(user=user, project=project, fields=fields)
        elif 'pagure.project.user.added' in msg['topic']:
            new_user = msg['msg']['new_user']
            tmpl = self._(
                '{user} added "{new_user}" to project {project}'
            )
            return tmpl.format(user=user, project=project, new_user=new_user)
        elif 'pagure.project.tag.removed' in msg['topic']:
            tags = msg['msg']['tags']
            tags = fedmsg.meta.base.BaseConglomerator.list_to_series(tags)
            tmpl = self._(
                '{user} removed tags "{tags}" from project {project}'
            )
            return tmpl.format(user=user, project=project, tags=tags)
        elif 'pagure.project.tag.edited' in msg['topic']:
            old_tag = msg['msg']['old_tag']
            new_tag = msg['msg']['new_tag']
            tmpl = self._(
                '{user} altered tags on project {project} from '
                '"{old_tag}" to "{new_tag}"'
            )
            return tmpl.format(
                user=user, project=project,
                old_tag=old_tag, new_tag=new_tag)
        elif 'pagure.project.forked' in msg['topic']:
            old_project = msg['msg']['project']['parent']['name']
            tmpl = self._(
                '{user} forked project "{old_project}" to "{project}"'
            )
            return tmpl.format(
                user=user, old_project=old_project, project=project)
        elif 'pagure.pull-request.comment.added' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            tmpl = self._(
                '{user} commented on pull-request#{id} of project '
                '"{project}"'
            )
            return tmpl.format(user=user, id=prid, project=project)
        elif 'pagure.pull-request.closed' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            merged = msg['msg']['merged']
            if merged:
                tmpl = self._(
                    '{user} merged pull-request#{id} of project '
                    '"{project}"'
                )
            else:
                tmpl = self._(
                    '{user} closed (without merging) pull-request#{id} '
                    'of project "{project}"'
                )
            return tmpl.format(user=user, id=prid, project=project)
        elif 'pagure.pull-request.new' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            title = msg['msg']['pullrequest']['title']
            tmpl = self._(
                '{user} opened pull-request#{id}: "{title}" on '
                'project "{project}"'
            )
            return tmpl.format(
                user=user, id=prid, project=project, title=title)
        elif 'pagure.pull-request.flag.added' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            username = msg['msg']['flag']['username']
            comment = msg['msg']['flag']['comment']
            tmpl = self._(
                '{username} flagged {project}#{id} with "{comment}"'
            )
            return tmpl.format(
                username=username, id=prid, comment=comment, project=project)

        elif 'pagure.pull-request.flag.updated' in msg['topic']:
            prid = msg['msg']['pullrequest']['id']
            username = msg['msg']['flag']['username']
            comment = msg['msg']['flag']['comment']
            tmpl = self._(
                '{username} updated the flags on {project}#{id} with: '
                '"{comment}"'
            )
            return tmpl.format(
                username=username, id=prid, comment=comment, project=project)
        elif 'pagure.git.receive' in msg['topic']:
            repo = self.__get_project(msg['msg']['commit'], key='repo')
            email = msg['msg']['commit']['email']
            user = email2fas(email, **config)
            summ = msg['msg']['commit']['summary']
            whole = msg['msg']['commit']['message']
            if summ.strip() != whole.strip():
                summ += " (..more)"

            branch = msg['msg']['commit']['branch']
            if 'refs/heads/' in branch:
                branch = branch.replace('refs/heads/', '')
            tmpl = self._('{user} pushed to {repo} ({branch}). "{summary}"')
            return tmpl.format(user=user or email, repo=repo,
                               branch=branch, summary=summ)

        else:
            pass

    def secondary_icon(self, msg, **config):
        username = msg['msg'].get('agent')
        if username:
            return avatar_url(username)
        else:
            return None

    def usernames(self, msg, **config):
        username = msg['msg'].get('agent')
        if not username and 'pagure.git.receive' in msg['topic']:
            email = msg['msg']['commit']['email']
            username = email2fas(email, **config)

        if username:
            return set([username])
        else:
            return set([])

    def objects(self, msg, **config):
        try:
            project = self.__get_project(msg['msg'])
        except KeyError:
            try:
                project = self.__get_project(msg['msg']['pullrequest'])
            except KeyError:
                project = "(unknown)"

        if 'pagure.project' in msg['topic']:
            return set([
                'project/%s' % project,
            ])
        elif 'pagure.issue' in msg['topic']:
            return set([
                'issue/%s' % msg['msg']['issue']['id'],
                'project/%s' % project,
            ])
        elif 'pagure.pull-request' in msg['topic']:
            return set([
                'pull-request/%s' % msg['msg']['pullrequest']['id'],
                'project/%s' % project,
            ])
        elif 'pagure.git.receive' in msg['topic']:
            project = self.__get_project(msg['msg']['commit'], key='repo')
            return set([
                'project/%s' % project,
            ])

        return set([])
