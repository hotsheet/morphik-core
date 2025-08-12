import logging
import zipfile
from typing import List, Tuple
from io import BytesIO

logger = logging.getLogger(__name__)

class ZipExtractionService:
    """Service for extracting and processing zip files"""
    
    def __init__(self, max_files: int = 100, max_total_size: int = 100 * 1024 * 1024):
        """Initialize zip extraction service
        
        Args:
            max_files: Maximum number of files to extract from zip
            max_total_size: Maximum total uncompressed size in bytes (default 100MB)
        """
        self.max_files = max_files
        self.max_total_size = max_total_size
    
    async def extract_zip(self, zip_content: bytes, original_filename: str) -> List[Tuple[str, bytes, str]]:
        """Extract files from zip archive
        
        Args:
            zip_content: Zip file content as bytes
            original_filename: Original zip filename
            
        Returns:
            List of tuples: (filename, file_content, mime_type)
            
        Raises:
            ValueError: If zip is invalid, too large, or contains too many files
        """
        try:
            with zipfile.ZipFile(BytesIO(zip_content), 'r') as zip_file:
                total_size = 0
                file_count = 0
                
                extracted_files = []
                
                for file_info in zip_file.filelist:
                    if file_info.is_dir():
                        continue
                        
                    file_count += 1
                    if file_count > self.max_files:
                        raise ValueError(f"Zip contains too many files (>{self.max_files})")
                    
                    total_size += file_info.file_size
                    if total_size > self.max_total_size:
                        raise ValueError(f"Zip uncompressed size too large (>{self.max_total_size} bytes)")
                    
                    try:
                        file_content = zip_file.read(file_info.filename)
                        
                        import filetype
                        kind = filetype.guess(file_content)
                        mime_type = kind.mime if kind else "application/octet-stream"
                        
                        extracted_files.append((file_info.filename, file_content, mime_type))
                        logger.debug(f"Extracted {file_info.filename} ({len(file_content)} bytes)")
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract {file_info.filename}: {e}")
                        continue
                
                logger.info(f"Successfully extracted {len(extracted_files)} files from {original_filename}")
                return extracted_files
                
        except zipfile.BadZipFile:
            raise ValueError("Invalid or corrupted zip file")
        except Exception as e:
            logger.error(f"Error extracting zip {original_filename}: {e}")
            raise ValueError(f"Failed to extract zip: {str(e)}")
