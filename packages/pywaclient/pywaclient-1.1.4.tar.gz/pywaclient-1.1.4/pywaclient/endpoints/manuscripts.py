#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from typing import Dict, Any

from pywaclient.endpoints import Endpoint


class ManuscriptEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'manuscript'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific manuscript.

        :param identifier:  The identifier of the manuscript.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Manuscript metadata
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new manuscript. Required parameters for the creation of this entity are "title" and "world.id".

        {
            "title":"Manuscript Title",
            "world":{
                "id": "{{worldId}}"
            }
        }

        :param content:     Metadata of the new manuscript with at least he required fields.
        :return:            Metadata of the created manuscript with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a manuscript.

        :param identifier:  The id of the manuscript to be updated.
        :param content:     All the fields that should be updated.
        :return:            Metadata of the manuscript.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a manuscript.

        :param identifier:  The id of the manuscript to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})
