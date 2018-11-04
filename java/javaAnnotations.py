JAVA_ANNOTATIONS = {}
JAVA_ANNOTATIONS['primary'] = ['@Id', '@GeneratedValue(strategy = GenerationType.AUTO)']
JAVA_ANNOTATIONS['@OneToOne'] = ['@OneToOne']
JAVA_ANNOTATIONS['@ManyToOne'] = ['@ManyToOne']
JAVA_ANNOTATIONS['@OneToMany'] = ['@OneToMany']
JAVA_ANNOTATIONS['@ManyToMany'] = ['@ManyToMany']

def annotationsFor(metaData, javaProperty):
    metaData = metaData.lower()
    annotations = []
    for key in JAVA_ANNOTATIONS:
        if key.lower() in metaData:
            for annotation in JAVA_ANNOTATIONS[key]:
                annotations.append(annotation)
    return annotations