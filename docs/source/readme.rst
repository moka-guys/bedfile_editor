readme
======

User Guide
==========

Welcome to the Bedmaker tool. Its purpose is to aid Genomic Scientists in creating bed files for use in clinical diagnostics.

It allows you to choose the exact transcripts you want to include for each gene in the bed file including the ability to specify padding, whether to include UTRs, and include introns.It suggests the most clinically relevant transcript for each gene, helping you make informed decisions.Once you are happy with your selection you can easily export bed files in a range of formats.It provides a a permanent and accessible record of the regions used in a clinical diagnostic which can be linked to clinical reports.

Overview: Creating a Bed File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Create a BedFileRequest by providing a list of gene IDs and setting global parameters such as whether to include UTRs or exan padding.
2. For each gene, either accept the suggested Ensembl Transcript to use, or manually select the most clinically appropriate transcript.Manually adjust the parameters for individual transcripts as required, on a case-by-case basis.
3. Manually adjust the parameters for individual transcripts as required, on a case-by-case basis.
4. Publish the bed file so that a permanent record of that version is created.
5. Send the bed file request for review & authorisation.
6. Once authorised export the bed file in the required format (4 column, 8 column etc).

Getting Started
^^^^^^^^^^^^^^^

The starting point for making a bed file is to create a BedFileRequest using the Import page of the tool.

The BedFileRequest is where you define the global parameters you want to apply to the final bed file, for example: - A list of Ensembl gene IDs which should be included. - Whether padding of exons is required - Whether to include UTRs

Choosing the transcript
^^^^^^^^^^^^^^^^^^^^^^^
The Edit page of the tool is used to select the most clinically appropriate transcript for each gene and, also to tweak parameters on a transcript-by-transcript basis.

Automated Transcript Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A suggestion of the most clinically relevant transcript is made for each gene following prioritisation as per the criteria below: 1. The RefSeq or MANE Select transcript, and RefSeq HGMD transcript. 2. RefSeq or MANE Select transcript, and the transcript covers all known ClinVar variants in gene. 3. RefSeq HGMD transcript, and transcript covers all known ClinVar variants in gene. 4. Coding transcript (enables prioritisation of singleton transcripts).

No action is required to accept the suggested transcript for a gene

Manual Transcript Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Overriding the suggested transcript for a gene, and/or selecting multiple transcripts for a gene can be done by selecting the tick box in the Selected column of the table.

Refining the choices per transcript
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

External APIs 
^^^^^^^^^^^^^

RefSeq Select – Subset of RefSeq Curated, a single Select transcript is chosen as representative for each protein-coding gene.

MANE transcript - Subset of RefSeq Select transcripts categorized as MANE, which are agreed upon as representative by both NCBI RefSeq and Ensembl/GENCODE, and have a 100% identical match to a transcript in the Ensembl annotation.

RefSeq HGMD – Subset of RefSeq Curated, transcripts annotated by the Human Gene Mutation Database.