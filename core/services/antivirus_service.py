import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class AntivirusService:
    """Service for scanning files with ClamAV antivirus"""
    
    def __init__(self, clamd_socket: Optional[str] = None):
        """Initialize antivirus service
        
        Args:
            clamd_socket: Path to ClamAV daemon socket, defaults to /var/run/clamav/clamd.ctl
        """
        self.clamd_socket = clamd_socket or "/var/run/clamav/clamd.ctl"
        self._client = None
    
    def _get_client(self):
        """Get ClamAV client, creating if needed"""
        if self._client is None:
            try:
                import clamd
                self._client = clamd.ClamdUnixSocket(self.clamd_socket)
                self._client.ping()
            except ImportError:
                logger.warning("clamd package not available, skipping virus scan")
                self._client = None
            except Exception as e:
                logger.warning(f"ClamAV not available: {e}")
                self._client = None
        return self._client
    
    async def scan_file(self, file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
        """Scan file content for viruses
        
        Args:
            file_content: File content as bytes
            filename: Original filename for logging
            
        Returns:
            Tuple of (is_clean, threat_name)
            is_clean: True if file is clean, False if infected
            threat_name: Name of detected threat if infected, None if clean
        """
        client = self._get_client()
        if client is None:
            logger.warning("ClamAV not available, skipping virus scan")
            return True, None
            
        try:
            result = client.instream(file_content)
            
            if result['stream'] == ('OK', None):
                logger.debug(f"File {filename} passed virus scan")
                return True, None
            else:
                threat_name = result['stream'][1] if len(result['stream']) > 1 else "Unknown threat"
                logger.warning(f"File {filename} failed virus scan: {threat_name}")
                return False, threat_name
                
        except Exception as e:
            logger.error(f"Error scanning file {filename}: {e}")
            return False, f"Scan error: {str(e)}"
