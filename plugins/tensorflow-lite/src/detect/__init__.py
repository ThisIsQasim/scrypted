from __future__ import annotations

import asyncio
from typing import Any, Tuple

import scrypted_sdk
from scrypted_sdk.types import (MediaObject, ObjectDetection,
                                ObjectDetectionCallbacks,
                                ObjectDetectionGeneratorSession,
                                ObjectDetectionModel, ObjectDetectionSession,
                                ObjectsDetected, ScryptedMimeTypes, Setting)


class DetectPlugin(scrypted_sdk.ScryptedDeviceBase, ObjectDetection):
    def __init__(self, nativeId: str | None = None):
        super().__init__(nativeId=nativeId)
        self.loop = asyncio.get_event_loop()

    def getClasses(self) -> list[str]:
        pass

    def getTriggerClasses(self) -> list[str]:
        pass

    def get_input_details(self) -> Tuple[int, int, int]:
        pass

    def get_input_format(self) -> str:
        pass

    def getModelSettings(self, settings: Any = None) -> list[Setting]:
        return []

    async def getDetectionModel(self, settings: Any = None) -> ObjectDetectionModel:
        d: ObjectDetectionModel = {
            'name': self.pluginId,
            'classes': self.getClasses(),
            'triggerClasses': self.getTriggerClasses(),
            'inputSize': self.get_input_details(),
            'inputFormat': self.get_input_format(),
            'settings': [],
        }

        d['settings'] += self.getModelSettings(settings)

        return d

    def get_detection_input_size(self, src_size):
        pass

    async def run_detection_videoframe(self, videoFrame: scrypted_sdk.VideoFrame, detection_session: ObjectDetectionSession) -> ObjectsDetected:
        pass
    
    async def generateObjectDetections(self, videoFrames: Any, session: ObjectDetectionGeneratorSession = None) -> Any:
        try:
            videoFrames = await scrypted_sdk.sdk.connectRPCObject(videoFrames)
            async for videoFrame in videoFrames:
               videoFrame = await scrypted_sdk.sdk.connectRPCObject(videoFrame)
               detected = await self.run_detection_videoframe(videoFrame, session)
               yield {
                   '__json_copy_serialize_children': True,
                   'detected': detected,
                   'videoFrame': videoFrame,
               }
        finally:
            try:
                await videoFrames.aclose()
            except:
                pass

    async def detectObjects(self, mediaObject: MediaObject, session: ObjectDetectionSession = None, callbacks: ObjectDetectionCallbacks = None) -> ObjectsDetected:
        vf: scrypted_sdk.VideoFrame
        if mediaObject and mediaObject.mimeType == ScryptedMimeTypes.Image.value:
            vf = mediaObject
        else:
            vf = await scrypted_sdk.mediaManager.convertMediaObjectToBuffer(mediaObject, ScryptedMimeTypes.Image.value)

        return await self.run_detection_videoframe(vf, session)
