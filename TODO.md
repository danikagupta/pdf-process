1. Keep it tab-based for the time-beiinng, but set the code to be be ready to create a multi-page App (every tab core code in a separate file)

2. Define file storage for keeping:
  a. Original docs : DONE
  b. PDF page-by-page (rely on file naming convention?) : DONE
  c. Generated embeddings (should this be FAISS store per model?)

3. Define one Tab for running  experiemnts by hand - this is useful when adding a new model.

4. Define one Tab for file uploads (already existing).Can we add support for CSV file with remote URLs? : DONE. Not needed at this time.

5. Define one Tab for all file processing - this should including functionality to regenerate everything, just given the source PDF files.

6. Define one Tab for running experiments using a Graph - this will run all the models available.This should include Langsmith as well.

What are the different embeddings possible?
1. No embedding - just convert PDF to list of PNG files and go. How is the order taken into account?
2. PyPDF text extraction
3. UnstructedIO extraction
4. Should we use Image Embeddings? Why?
