# Credit: Parts of this app are inspired by Chanin Nantasenamat (Data Professor) https://youtube.com/dataprofessor


# To create interactive web applications
import streamlit as st
# To make interactive molecular visualizations
# and to display molecular structures
from stmol import showmol
# For molecular structures in 3D
import py3Dmol
# To make HTTP requiest
import requests
# Computational molecular biology
import biotite.structure.io as bsio
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Side bar and its description
st.sidebar.title('ESMFold')
st.sidebar.write("This predictor is limited to 400 aminoacids")

# To give the option to choose different styles for the model
visualization_styles = ['line', 'stick', 'sphere', 'cartoon', 'cross']
visual_style = st.sidebar.selectbox("Choose visualization style", visualization_styles)

# stmol
def render_mol(pdb):
    # To avoid bugs or errors
    if not pdb:
        raise ValueError("Invalid PBD object")
    # New variable pbdview that creates a 3D viewer model
    pdbview = py3Dmol.view()
    # Adds the pbd model to the viewer
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({visual_style:{'color':'spectrum'}})
    pdbview.setBackgroundColor('black')
    pdbview.zoomTo()
    pdbview.zoom(2, 800) #Zoom in
    showmol(pdbview, height = 500,width=800) # Size

# Protein sequence input, the DEFAULT_SEQ is G protein [Glycine max], CAA64834.1
DEFAULT_SEQ = "MGLLCSRNRRYNDADAEENAQTAEIERRIEVRNERAEKHIQKLLLLGAGESGKSTIFKQIKLLFQTGFDEAELKSYLPVIHANVYQTIKLLHDGSKEFAQNDVDSSKYVISNENKEIGEKLLEIGGRLDYPYLSKELAQEIENLWKDPAIQETYARGSELQIPDCTDYFMENLQRLSDANYVPTKEDVLYARVRTTGVVEIQFSPVGENKKSDEVYRLFDVGGQRNERRKWIHLFEGVSAVIFCAAISEYDQTLFEDENRNRMMETKELFEWILKQPCFEKTSFMLFLNKFDIFEKKILKVPLNVCEWFKDYQPVSTGKQEIEHAYEFVKKKFEESYFQSTAPDRVDRVFKIYRTTALDQKVVKKTFKLVDETLRRRNLLEAGLL"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=350)

def validate_sequence(sequence):
    valid_aa = 'ACDEFGHIKLMNPQRSTVWY'
    if len(sequence) > 400:
        st.error("Sequence is too long. Please enter a sequence of 400 amino acids or less.")
        return False
    for aa in sequence:
        if aa not in valid_aa:
            st.error("Invalid sequence. Please enter a valid protein sequence.")
            return False
    return True
    
# ESMfold
def update(sequence=txt):
    # Content-Type tells what kind of data is sending the client to the server
    # "application/x-www-form-urlencoded" is to send alfanumeric data
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    # POST resquest a server to accept the data enclossed in the body of the request message
    # "https://api.esmatlas.com/foldSequence/v1/pdb/" this URL is where ESMFold API returns the 3D structures
    # Since aprox oct 2023, there is a SSL certification failure with ESMFold, until that is corrected, we are going to disable the SSL certificate check with "verify = False"
    # You should avoid doing that because it makes your app vulnerable to hacking, like 'man-in-the-middle' attacks
    # We are doing it to test the app
    validate_sequence(sequence)
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence, verify = False)
    name = sequence[:3] + sequence[-3:] # Name with the first 3 and last 3 letters of the seq
    pdb_string = response.content.decode('utf-8') # Decodes from bytes to string

    if pdb_string.strip():
        with open('predicted.pdb', 'w') as f: # Open file in write mode
            f.write(pdb_string) #writes pdb_string in file "f"

        struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"]) # Loads structure and b_value
        b_value = round(struct.b_factor.mean(), 4) # Calculates b_value

        # Display protein structure
        st.subheader("Visualization of predicted protein structure")
        render_mol(pdb_string)

        st.subheader("plDDT")
        st.write("plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.")
        st.info(f'plDDT: {b_value}')

        analysis = ProteinAnalysis(txt)
        mw = round(analysis.molecular_weight(), 4)
        iso_point = round(analysis.isoelectric_point(), 4)
        secondary_str_fact = tuple(round(value, 4) for value in analysis.secondary_structure_fraction())
        st.subheader("Protein Analysis")
        st.write("Calculates the molecular weight, isoelectric point and secondary structure fraction")
        st.info(f'Molecular weight: {mw}')
        st.info(f'Isoelectric point: {iso_point}')
        st.info(f'Secondary structure fraction: {secondary_str_fact}')

        st.download_button(
            label = "Download PDB",
            data = pdb_string,
            file_name = 'predicted_protein.pdb',
            mime = 'text/plain',
    )
    else:
        st.error("Please try again with a valid sequence")


with st.spinner('Predicting...'):
    predict = st.sidebar.button('Predict', on_click=update) # Predict button


if not predict:
    st.warning('👈 Enter protein sequence data!')
