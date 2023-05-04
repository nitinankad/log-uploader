from abc import ABC, abstractmethod

class LogUploader:
	@abstractmethod
	def upload_logs(self, title, log_data):
		pass
