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
from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.survey.fhir_pb2_grpc import FHIRStub


class FHIR(BaseServicesInterface):
    """
    A class representing the Calls service interface.

    This class provides methods to interact with the Calls service, which allows starting and managing
    callers, listeners, scheduled callers, and handling calls and audio files.

    Inherits from BaseServicesInterface.
    """

    @property
    def stub(self) -> FHIRStub:
        """
        Get the gRPC stub for the Calls service.

        Returns:
            CallsStub: The gRPC stub for the Calls service.
        """
        stub: FHIRStub = FHIRStub(channel=self.grpc_channel)
        return stub
