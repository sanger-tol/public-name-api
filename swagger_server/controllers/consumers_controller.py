from swagger_server.model import db, PnaSpecies, PnaSpecimen, PnaUser
from flask import jsonify
from swagger_server.db_utils import create_new_specimen

def search_specimen(specimen_id=None, skip=None, limit=None):  
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimens = db.session.query(PnaSpecimen).filter(PnaSpecimen.specimen_id == specimen_id).all()

    if not specimens:
        return jsonify([])

    # This can be simplified once the model can be changed
    tolIds = []
    for specimen in specimens:
        tolId = {'tolId': specimen.public_name,
                'species': specimen.species}
        tolIds.append(tolId)
    return jsonify([{'specimenId': specimen_id,
                    'tolIds': tolIds}])

def search_tol_id(tol_id=None, skip=None, limit=None):  
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.public_name == tol_id).one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])

def search_tol_id_by_taxon_specimen(taxonomy_id=None, specimen_id=None, skip=None, limit=None):  
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.species_id == taxonomy_id).filter(PnaSpecimen.specimen_id == specimen_id).one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])

def bulk_search_specimens(body=None, api_key=None):  
    """searches DToL ToLIDs in bulk

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param bosy: 
    :type taxonomyId: str

    :rtype: List[Specimen]
    """
    user = db.session.query(PnaUser).filter(PnaUser.api_key == api_key).one_or_none()
    specimens = []
    # body contains the rows of data
    if body:
        for row in body:
            specimen_id = row['specimenId']
            taxonomy_id = row['taxonomyId']
            species = db.session.query(PnaSpecies).filter(PnaSpecies.taxonomy_id == taxonomy_id).one_or_none()

            if species is None:
                return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

            specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.specimen_id == specimen_id).one_or_none()

            if specimen is not None:
                if specimen.species.taxonomy_id != species.taxonomy_id:
                    return "Species of specimen "+str(specimen_id)+" is "+ specimen.species.name + " but was expecting "+species.name, 400
            else:
                specimen = create_new_specimen(species, specimen_id, user)

            specimens.append(specimen)

        for specimen in specimens:
            db.session.add(specimen)
        db.session.commit()

    return jsonify(specimens)

def search_species(taxonomy_id=None, skip=None, limit=None):  
    """searches species

    By passing in the appropriate taxonomy string, you can search for available species in the system 

    :param taxonomyId: pass an optional taxonomy ID to filter by
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Species]
    """

    species = db.session.query(PnaSpecies).filter(PnaSpecies.taxonomy_id == taxonomy_id).one_or_none()

    if species is None:
        return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

    return jsonify([species])
