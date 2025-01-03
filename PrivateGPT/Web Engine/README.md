# PrivateGPT New Setup

Follow the instructions in the client and server directories to set up the PrivateGPT app for OPA.

**LLM used** - [Salesforce/codet5-small](https://huggingface.co/Salesforce/codet5-small)

# Containerized Setup Instructions

1. Make a new directory within privategpt_server directory - `mkdir -p privategpt_server/codet5_fine_tuned`.
2. Merge the codet5 split files in the privategpt_server/codet5_fine_tuned_split/ directory with `cat privategpt_server/codet5_fine_tuned_split/codet5-fine-tuned.ckpt* > privategpt_server/codet5_fine_tuned/codet5-fine-tuned.ckpt`.
3. Run the docker compose file with `docker-compose up -d`.
4. Test the app on `http://localhost:3000`.
