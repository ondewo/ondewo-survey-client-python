# Copyright 2021-2024 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from ondewo.utils.async_base_services_interface import AsyncBaseServicesInterface

from ondewo.survey.survey_pb2_grpc import SurveysStub


class Survey(AsyncBaseServicesInterface):
    """
    A class representing the Projects service interface.

    This class provides methods to interact with the Projects service, which allows managing VtsiProjects.

    Inherits from BaseServicesInterface.
    """

    @property
    def stub(self) -> SurveysStub:
        """
        Get the gRPC stub for the Projects service.

        Returns:
            ProjectsStub: The gRPC stub for the Projects service.
        """
        stub: SurveysStub = SurveysStub(channel=self.grpc_channel)
        return stub
