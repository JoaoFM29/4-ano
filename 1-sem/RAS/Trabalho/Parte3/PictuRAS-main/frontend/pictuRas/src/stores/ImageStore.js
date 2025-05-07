import { defineStore } from 'pinia';
import JSZip from 'jszip';
import axios from 'axios';

const api =
    import.meta.env.VITE_API_GATEWAY;

export const useImageStore = defineStore('imageStore', {
    state: () => ({
        images: [], // depois vai ser vazia
        bytes: [],
        old: [],
        ids: [],
        selectedImage: null,
        previewMode: false,
        onProcess: false,
    }),
    actions: {
        selectImage(image) {
            this.selectedImage = image;
        },
        async fetchImages(projectId) {
            this.loading = true;
            this.error = null;
            try {
                this.image = [];
                this.ids = [];
                this.selectedImage = null;
                const response = await axios.get(`${api}/api/projects/images`, {
                    params: { projectId: projectId }, // Pass query params
                    withCredentials: true // Include credentials if needed (cookies, headers)
                });
                this.ids = response.data.map((element) => element.id);
                let imageUrls = [];
                let imageBlobs = [];

                // Iterate through each image element returned by the API
                for (const element of response.data) {
                    try {
                        // Fetch the actual image as an ArrayBuffer
                        const response2 = await axios.get(`${api}/api/projects/images/${element.id}`, {
                            responseType: 'arraybuffer'
                        });

                        // Extract MIME type from response headers
                        const mimeType = response2.headers['content-type'];

                        // Create a Blob using the ArrayBuffer and MIME type
                        const blob = new Blob([response2.data], { type: mimeType });

                        // Generate an object URL for the image Blob
                        const imageSrc = URL.createObjectURL(blob);

                        // Store the image source URL and blob
                        imageUrls.push(imageSrc);
                        imageBlobs.push(blob);
                    } catch (error) {
                        console.log("Error fetching image:", error);
                    }
                }

                // Update the store state
                this.images = imageUrls; // URLs for displaying images
                this.bytes = imageBlobs; // Blobs for downloading images
            } catch (error) {
                console.error("Error fetching images:", error);
            } finally {
                this.loading = false;
            }
        },
        async downloadAllImagesAsZip(projectId) {
            if (this.bytes.length === 0) {
                console.error("No images available for download.");
                return;
            }

            const zip = new JSZip(); // Create a new ZIP file instance

            // Add each blob to the ZIP
            for (let i = 0; i < this.bytes.length; i++) {
                const blob = this.bytes[i];
                zip.file(`image-${i + 1}.jpg`, blob); // Add the blob as a file
            }

            try {
                // Generate the ZIP file asynchronously
                const zipBlob = await zip.generateAsync({ type: 'blob' });

                // Create a temporary object URL for the ZIP blob
                const url = URL.createObjectURL(zipBlob);

                // Create a temporary <a> element
                const a = document.createElement('a');
                a.href = url;
                a.download = `${projectId}-images.zip`; // Name of the downloaded ZIP file
                document.body.appendChild(a);
                a.click(); // Trigger the download

                // Cleanup
                document.body.removeChild(a); // Remove the anchor element
                URL.revokeObjectURL(url); // Revoke the object URL to free up memory
            } catch (error) {
                console.error("Error creating ZIP file:", error);
            }
        },
        clear() {
            this.images = [];
            this.bytes = [];
            this.ids = [];
            this.selectedImage = null;
        },
        enterProcessMode() {
            this.onProcess = true;
            this.images = [];
            this.old = this.bytes;
        },
        leaveProcessMode(cancel) {
            if (!cancel) {
                this.onProcess = false;
            } else {

                this.onProcess = false;
            }
            console.log(this.onProcess)
        },
        async updateList(images) {
            try {

                for (const element of images) {
                    try {

                        // Extract MIME type from response headers
                        // Create a Blob using the ArrayBuffer and MIME type
                        const binaryString = atob(element.data);

                        // Create an ArrayBuffer of the same length as the binary string
                        const arrayBuffer = new ArrayBuffer(binaryString.length);

                        // Create a Uint8Array view to manipulate the ArrayBuffer
                        const uint8Array = new Uint8Array(arrayBuffer);

                        // Fill the Uint8Array with the binary string's char codes
                        for (let i = 0; i < binaryString.length; i++) {
                            uint8Array[i] = binaryString.charCodeAt(i);
                        }
                        // if texto, download
                        if (element.mimetype === 'plain/text') {
                            // Create a Blob from the ArrayBuffer
                            const blob = new Blob([arrayBuffer], { type: 'text/plain' });

                            // Create a URL for the Blob
                            const url = URL.createObjectURL(blob);

                            // Create an anchor element and set attributes for download
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = 'downloaded_text.txt'; // Default file name

                            // Append the anchor to the body, click it, and remove it
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);

                            // Release the Blob URL to free memory
                            URL.revokeObjectURL(url);

                            return; // Return if necessary
                        }

                        const blob = new Blob([arrayBuffer], { type: element.mimetype });
                        // Generate an object URL for the image Blob
                        const imageSrc = URL.createObjectURL(blob);

                        // Store the image source URL and blob
                        this.images.push(imageSrc);
                        this.bytes.push(blob);
                        this.ids.push(element.id)
                    } catch (error) {
                        console.log("Error fetching image:", error);
                    }
                }

            } catch (error) {
                console.log("Error fetching image:", error);
            }

        },
        async deleteImages(projectId, imageIds) {
            // Send delete request to the API
            try {
                console.log(`${api}/api/projects/images`);
                const response = await axios.delete(`${api}/api/projects/images`, {
                    params: { projectId: projectId, images: imageIds }, // Pass query params
                    withCredentials: true // Include credentials if needed (cookies, headers)
                });

                await this.fetchImages(projectId);
                console.log("here")
            } catch (e) {
                console.log(e)
            }
        },
        enterPreviewMode() {
            this.previewMode = true;
        },
        leavePreviewMode(cancel) {
            if (!cancel) {
                this.previewMode = false;
            } else {
                this.previewMode = false;
            }
        },
        getSelectedImageId() {
            if (this.selectedImage) {
                const selectedIndex = this.images.indexOf(this.selectedImage);
                if (selectedIndex !== -1) {
                    return this.ids[selectedIndex]; // Return the ID corresponding to the selected image
                }
            }
            return null; // Return null if no image is selected or if the image is not found
        },
        async updateSelectedImage(images) {
            try {
                try {
                    // Extract MIME type from response headers
                    // Create a Blob using the ArrayBuffer and MIME type
                    const element = images[0];
                    const binaryString = atob(element.data);

                    // Create an ArrayBuffer of the same length as the binary string
                    const arrayBuffer = new ArrayBuffer(binaryString.length);

                    // Create a Uint8Array view to manipulate the ArrayBuffer
                    const uint8Array = new Uint8Array(arrayBuffer);

                    // Fill the Uint8Array with the binary string's char codes
                    for (let i = 0; i < binaryString.length; i++) {
                        uint8Array[i] = binaryString.charCodeAt(i);
                    }
                    if (element.mimetype === 'plain/text') {
                        // Create a Blob from the ArrayBuffer
                        const blob = new Blob([arrayBuffer], { type: 'text/plain' });

                        // Create a URL for the Blob
                        const url = URL.createObjectURL(blob);

                        // Create an anchor element and set attributes for download
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'downloaded_text.txt'; // Default file name

                        // Append the anchor to the body, click it, and remove it
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);

                        // Release the Blob URL to free memory
                        URL.revokeObjectURL(url);

                        return; // Return if necessary
                    }


                    const blob = new Blob([arrayBuffer], { type: element.mimetype });
                    // Generate an object URL for the image Blob
                    const imageSrc = URL.createObjectURL(blob);

                    // Store the image source URL and blob

                    this.selectedImage = imageSrc; // Properly update the selectedImage
                } catch (error) {
                    console.log("Error fetching image:", error);
                }


            } catch (error) {
                console.log("Error fetching image:", error);
            }

        },
        canPreview() {
            if (this.selectedImage && !this.previewMode)
                return this.images.includes(this.selectedImage)
            else
                return false;
        }
    },
});