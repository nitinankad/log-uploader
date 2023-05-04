from abc import ABC, abstractmethod

class LogUploader(ABC):
	@abstractmethod
	def upload_logs(self, log_data):
		pass
