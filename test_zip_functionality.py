import asyncio
import zipfile
import os
from io import BytesIO
from core.services.zip_service import ZipExtractionService
from core.services.antivirus_service import AntivirusService

async def test_zip_extraction():
    """Test zip file extraction functionality"""
    print("Testing zip extraction...")
    
    test_files = {
        'test.txt': b'This is a test text file content.',
        'sample.md': b'# Sample Markdown\n\nThis is a markdown file.',
        'data.json': b'{"name": "test", "value": 123}'
    }

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in test_files.items():
            zip_file.writestr(filename, content)

    with open('test_upload.zip', 'wb') as f:
        f.write(zip_buffer.getvalue())

    print('Created test_upload.zip with files:', list(test_files.keys()))
    
    zip_service = ZipExtractionService()
    
    with open('test_upload.zip', 'rb') as f:
        zip_content = f.read()
    
    try:
        extracted_files = await zip_service.extract_zip(zip_content, 'test_upload.zip')
        print(f'Successfully extracted {len(extracted_files)} files:')
        for filename, content, mime_type in extracted_files:
            print(f'  - {filename} ({len(content)} bytes, {mime_type})')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False

async def test_antivirus():
    """Test antivirus scanning functionality"""
    print("\nTesting antivirus scanning...")
    
    antivirus_service = AntivirusService()
    
    test_content = b'This is a test file content.'
    is_clean, threat_name = await antivirus_service.scan_file(test_content, 'test.txt')
    
    print(f'File scan result: clean={is_clean}, threat={threat_name}')
    return True

async def main():
    """Run all tests"""
    print("Running zip functionality tests...\n")
    
    success1 = await test_zip_extraction()
    success2 = await test_antivirus()
    
    if success1 and success2:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    if os.path.exists('test_upload.zip'):
        os.remove('test_upload.zip')

if __name__ == "__main__":
    asyncio.run(main())
