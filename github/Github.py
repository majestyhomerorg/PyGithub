# Copyright 2012 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of PyGithub. http://vincent-jacques.net/PyGithub

# PyGithub is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with PyGithub.  If not, see <http://www.gnu.org/licenses/>.

from Requester import Requester
import AuthenticatedUser
import NamedUser
import Organization
import Gist
import PaginatedList
import Repository
import Legacy
import GithubObject

class Github( object ):
    def __init__( self, login_or_token = None, password = None ):
        self.__requester = Requester( login_or_token, password )

    @property
    def rate_limiting( self ):
        return self.__requester.rate_limiting

    def get_user( self, login = None ):
        if login is None:
            return AuthenticatedUser.AuthenticatedUser( self.__requester, { "url": "https://api.github.com/user" }, completed = False )
        else:
            headers, data = self.__requester.requestAndCheck(
                "GET",
                "https://api.github.com/users/" + login,
                None,
                None
            )
            return NamedUser.NamedUser( self.__requester, data, completed = True )

    def get_organization( self, login ):
        headers, data = self.__requester.requestAndCheck(
            "GET",
            "https://api.github.com/orgs/" + login,
            None,
            None
        )
        return Organization.Organization( self.__requester, data, completed = True )

    def get_gist( self, id ):
        headers, data = self.__requester.requestAndCheck(
            "GET",
            "https://api.github.com/gists/" + str( id ),
            None,
            None
        )
        return Gist.Gist( self.__requester, data, completed = True )

    def get_gists( self ):
        headers, data = self.__requester.requestAndCheck( "GET", "https://api.github.com/gists/public", None, None )
        return PaginatedList.PaginatedList(
            Gist.Gist,
            self.__requester,
            headers,
            data
        )

    def legacy_search_repos( self, keyword, language = GithubObject.NotSet ):
        assert isinstance( keyword, ( str, unicode ) ), keyword
        assert language is GithubObject.NotSet or isinstance( language, ( str, unicode ) ), language
        args = {} if language is GithubObject.NotSet else { "language": language }
        return Legacy.PaginatedList(
            "https://api.github.com/legacy/repos/search/" + keyword,
            args,
            self.__requester,
            "repositories",
            Legacy.convertRepo,
            Repository.Repository,
        )

    def legacy_search_users( self, keyword ):
        assert isinstance( keyword, ( str, unicode ) ), keyword
        return Legacy.PaginatedList(
            "https://api.github.com/legacy/user/search/" + keyword,
            {},
            self.__requester,
            "users",
            Legacy.convertUser,
            NamedUser.NamedUser,
        )

    def legacy_search_user_by_email( self, email ):
        assert isinstance( email, ( str, unicode ) ), email
        headers, data = self.__requester.requestAndCheck(
            "GET",
            "https://api.github.com/legacy/user/email/" + email,
            None,
            None
        )
        return NamedUser.NamedUser( self.__requester, Legacy.convertUser( data[ "user" ] ), completed = False )
