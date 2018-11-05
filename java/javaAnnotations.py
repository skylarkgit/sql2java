JAVA_ANNOTATIONS = {}
JAVA_ANNOTATIONS['primary'] = ['@Id', '@GeneratedValue(strategy = GenerationType.AUTO)']
JAVA_ANNOTATIONS['@OneToOne'] = ['@OneToOne', '@JoinColumn(name="{id}")']
JAVA_ANNOTATIONS['@ManyToOne'] = ['@ManyToOne', '@JoinColumn(name="{foreignId}")']
JAVA_ANNOTATIONS['@OneToMany'] = ['@OneToMany', '@JoinColumn(name="{foreignId}")']
JAVA_ANNOTATIONS['@ManyToMany'] = ['@ManyToMany','@JoinTable(name="{relationTable}", joinColumns=@JoinColumn(name="{foreignId}"), inverseJoinColumns=@JoinColumn(name="{localIdOfForeign}"))']
JAVA_ANNOTATIONS['@JsonIgnore'] = ['@JsonIgnore']
JAVA_ANNOTATIONS['@OneToOnForeign'] = ['@OneToOne(mappedBy="{varname}")', '@JsonIgnore']
def annotationsFor(metaData, annotateProperties):
    metaData = metaData.lower()
    annotations = []
    for key in JAVA_ANNOTATIONS:
        if key.lower() in metaData:
            for annotation in JAVA_ANNOTATIONS[key]:
                annotations.append(annotation.format(**annotateProperties))
    return annotations