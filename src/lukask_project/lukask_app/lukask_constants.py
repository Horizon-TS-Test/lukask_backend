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
