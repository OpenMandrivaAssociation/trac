#!/usr/bin/perl -w
#
# version 0.5
# Copyright (C) 2004-2005-2006-2007 Michael Scherer
# Author: Michael Scherer <misc@mandrake.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# TODO use a dedicated user ?
# use N() to translate

package MDK::Wizard::Trac;
use lib qw(/usr/lib/libDrakX);

use strict;
use services;
use common;
use Libconf;
use Libconf::Glueconf::Generic::Shell;

use MDK::Wizard::Wizcommon;
use File::Basename;

my $wiz = new MDK::Wizard::Wizcommon;
my $in = interactive->vnew;

my $TRAC_REPOSITORY_PATH_BASE = '/var/trac/project';
my $TRAC_TEMPLATE_PATH = '/usr/share/trac/templates';

my $o = {
    name => 'Trac Configuration Wizard',
    var => {
        PROJECT_NAME => 'test_project',
        # see the default value in subversion-server
        SVN_REPOSITORY_PATH => '/var/lib/svn/repositories/',
        TRAC_REPOSITORY_PATH => $TRAC_REPOSITORY_PATH_BASE,
        tracd_port => '8080'
    },
    # FIXME 
    defaultimage => "/usr/share/wizards//dns_wizard/images/DNS.png",
    # use standalone, less risk to screw a existing apache configuration.
    # and it is easier to setup
    needed_rpm => [ 'trac', 'trac-standalone', 'trac-sqlite', 'trac-svn'],
};

$o->{pages} = {
    welcome => {
        name => N("Trac configuration wizard") . "\n\n" . N("Trac is an integrated software project management, providing a wiki, a interface to browse subversion repository, and a bug tracking system.\n"),
        no_back => 1,
        data => [
        { label => N("Please enter the name of your project :"), val => \$o->{var}{PROJECT_NAME} },
        ],
        post => sub {
            my $p = lc($o->{var}{PROJECT_NAME});
            # FIXME extend the check
            $p =~ s/\s/_/g; 
            $p =~ s|/|_|g;
            $o->{var}{TRAC_REPOSITORY_PATH} = "$TRAC_REPOSITORY_PATH_BASE/$p";
            return 'trac_repo';
        },
        next => 'trac_repo',
    },
    trac_repo => {
        name => N("Trac repository"),
        data => [
        { label => N("Please enter the location of the trac repository :"), val => \$o->{var}{TRAC_REPOSITORY_PATH} },
        { label => N("This is different from the subversion repository, which will be used to store the source code of your project") },
        ],
        complete => sub {
            if (-d $o->{var}{TRAC_REPOSITORY_PATH})
            {
                $in->ask_warn("Error", "The directory already exist. You should remove it to create a trac repository..");
                return 1;
            }
            return 0;
        },
        next => 'svn_repo'
    },
    svn_repo => {
        name => N("Svn repository"),
        data => [
        { label => N("Please enter the location of the subversion repository ( will be created if it doesn't already exist ) :"), val => \$o->{var}{SVN_REPOSITORY_PATH} },
        ],
        complete => sub {
            return 0 if 
            system("svnlook info $o->{var}{SVN_REPOSITORY_PATH}  >/dev/null 2>&1");
            if ($?)
            {
                $in->ask_warn("Error", "This is not a proper subversion repository.");
                return 1;
            }
            return 0;
        },
        post => sub {
            return 'svn_creation' if ! -d $o->{var}{SVN_REPOSITORY_PATH};
            return 'trac_creation';
        }
    },
    svn_creation => {
        name => N("Svn repository creation"),
        data => [
        { label => N("The repository will now be created, with the command :\nsvnadmin create --fs-type fsfs $o->{var}{SVN_REPOSITORY_PATH}") },
        ],
        complete => sub {
            $in->do_pkgs->install('subversion-tools') if ! $in->do_pkgs->is_installed('subversion-tools');
            mkdir_p("$o->{var}{SVN_REPOSITORY_PATH}");
            # fsfs is choosed as bdb can lock under high load.
            system("svnadmin create --fs-type fsfs $o->{var}{SVN_REPOSITORY_PATH}");
            if ($?)
            {
                $in->ask_warn("Error", "The repository could not be created.");
                return 1;
            }
            return 0;
        },
        no_back => 1,
        next => 'trac_creation',
    },

    trac_creation => {
        name => N("Trac creation :"),
        data => [
        { label => N("Now, the trac repository will be created and configurated.") }
        ],
        complete => sub {
            my $_win = $in->wait_message("Repository creation","Trac repository is being created.");
            mkdir_p(dirname($o->{var}{TRAC_REPOSITORY_PATH}));
            system(qq(trac-admin "$o->{var}{TRAC_REPOSITORY_PATH}" initenv "$o->{var}{PROJECT_NAME}" "sqlite:db/trac.db" "svn" "$o->{var}{SVN_REPOSITORY_PATH}" "$TRAC_TEMPLATE_PATH" ));
            if ($?)
            {
                $in->ask_warn("Error", "The trac repository could not be created.");
                return 1;
            }

            my $conf = new Libconf::Glueconf::Generic::Shell({filename => '/etc/sysconfig/tracd'});
            $conf->{PROJECT} .= "$o->{var}{TRAC_REPOSITORY_PATH} ";
            $o->{var}{tracd_port} = $conf->{PORT};
            $conf->write_conf();

            if (services::is_service_running('tracd')) {
                services::restart('tracd')
            } else {
                services::start('tracd')
            }
            return 0;
        },
        no_back => 1,
        next => 'trac_summary'
    },

    trac_summary => {
        name => N("Trac setup summary"),
        data => [
        # maybe one day, html link ?
        { label => N("Your project can now be accessed  by using : \nhttp://localhost:$o->{var}{tracd_port}/$o->{var}{PROJECT_NAME}/\nYou can change the setting by editing /etc/sysconfig/trac, and by using trac-admin.\nMore info on the wiki http://trac.edgewall.com/.") },
        ],
        end => 1,
        next => 0,
    },
};

sub new {
    my ($class) = @_;
    bless $o, $class;
}

1;
