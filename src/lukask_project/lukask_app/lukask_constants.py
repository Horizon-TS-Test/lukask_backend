class LukaskConstants:
    """
    Contiene informacion de constantes que se maneja en la dase de datos lukask.
    """

    #-----------------------------------------#
    #   constantes para insercion en DB       #
    #-----------------------------------------#
    LOGICAL_STATE_ACTIVE                = True
    LOGICAL_STATE_INACTIVE              = False


    # -----------------------------------------#
    #   constantes para busqueda en DB         #
    # -----------------------------------------#
    TYPE_ACTION_RELEVANCE               = 'Relevancia'
    TYPE_ACTION_COMMENTS                = 'Comentario'
    FILTERS_ACTION_CHILDREN             = 'children'
    FILTERS_ACTION_COMMENTS             = 'comments'
    FILTERS_ACTION_REPLIES              = 'replies'
    USERS_RELEVANCE_PUBLICATION         = 'usrRelPub'
    USERS_RELEVANCE_COMMENT             = 'usrRelCom'
    FILTER_PROVINCE                     = 'province'
    FILTER_CANTON                       = 'canton'
    FILTER_PUBLICATION_USER             = 'pubUserQr'
    FILTER_PUBLICATION_TYPE             = 'pubTypeQr'
    FILTER_TYPEPUB_PUBLICATION          = '2742791e-8a99-48cb-bf22-2e0c342f0056'

    #-----FILTROS PARA PUBLICACION ----------#
    FILTER_SINCE_DATE                   = 'sinceDate'
    FILTER_UNTIL_DATE                   = 'untilDate'
    FILTER_LOCATION_PUB                 = 'locationPub'   

    # ----------------------------------------#
    #   FILTRO DE PERFILES                    #
    # ----------------------------------------#
    PROFILE_ADMIN                       = 'cf1f78a7-5e7e-4cd3-8d26-978bcb95e040'
    PROFILE_USER                        = 'ed5fd621-b7db-4567-9c09-c2336ce7b0bb'
