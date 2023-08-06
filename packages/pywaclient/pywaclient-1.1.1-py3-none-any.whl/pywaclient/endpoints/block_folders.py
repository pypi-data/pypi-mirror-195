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


class BlockEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'blockfolder'
        self.paths = 'blockfolders'

    def get(self, identifier: str, granularity: int) -> Dict[str, Any]:
        """Get the metadata of a specific blockfolder.

        :param identifier:  The identifier of the blockfolder.
        :param granularity: The granularity is between -1 and 2. Determines the amount of information returned by the
                            api.
        :return:            Block data
        """
        return self._get_request(self.path, {'id': identifier, 'granularity': str(granularity)})

    def put(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new block folder. Required parameters for the creation of this entity are "title" and "world".

        {
            "title":"Block Folder",
            "world": {
                "id":"{{worldId}}"
            }
        }

        :param content:     Data of the new block folder with at least the required fields.
        :return:            Data of the created block folder with the id.
        """
        return self._put_request(self.path, content)

    def patch(self, identifier: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (patch) the content of a block folder.

        {
            "title": "Updated Block"
        }

        :param identifier:  The id of the block folder to be updated.
        :param content:     All the fields that should be updated.
        :return:            Data of the block folder.
        """
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier: str):
        """
        Delete a block folder.

        :param identifier:  The id of the block folder to be deleted.
        """
        self._delete_request(self.path, {'id': identifier})


    def blocks(self, world_id: str, folder_id: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        List all statblocks by a world and folder id given, filtered with a limit of entities shown and an offset.

        :param world_id:    The id of the world the articles should be returned from.
        :param folder_id: The id of the category to return the articles from. To get articles without a category set
                            this value to -1.
        :param limit:       Determines how many articles are returned. Value between 1 and 50.
        :param offset:      Determines the offset at which articles are returned. Has to be a positive integer.
        :return:
        """
        return self._post_request(self.path,
                                  {'id': world_id},
                                  {'limit': limit, 'offset': offset, 'folder': {'id': folder_id}})
