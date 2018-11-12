JAVA_ANNOTATIONS = {}
JAVA_ANNOTATIONS['primary'] = ['@Id', '@GeneratedValue(strategy = GenerationType.IDENTITY)']
JAVA_ANNOTATIONS['@OneToOne'] = ['@OneToOne', '@JoinColumn(name="{id}")']
JAVA_ANNOTATIONS['@ManyToOne'] = ['@ManyToOne', '@JoinColumn(name="{foreignId}")']
JAVA_ANNOTATIONS['@OneToMany'] = ['@OneToMany(cascade = {{CascadeType.ALL}}, orphanRemoval=true)', '@JoinColumn(name="{foreignId}")']
JAVA_ANNOTATIONS['@ManyToMany'] = ['@ManyToMany','@JoinTable(name="{relationTable}", joinColumns=@JoinColumn(name="{foreignId}"), inverseJoinColumns=@JoinColumn(name="{localIdOfForeign}"))']
JAVA_ANNOTATIONS['@JsonIgnore'] = ['@JsonIgnore']
JAVA_ANNOTATIONS['@JsonWriteOnly'] = ['@JsonProperty(access = Access.WRITE_ONLY)']
JAVA_ANNOTATIONS['@OneToOnForeign'] = ['@OneToOne(mappedBy="{varname}", cascade = {{CascadeType.ALL}}, orphanRemoval=true)']

def annotationsFor(metaData, annotateProperties):
    metaData = metaData.lower()
    annotations = []
    for key in JAVA_ANNOTATIONS:
        if key.lower() in metaData:
            for annotation in JAVA_ANNOTATIONS[key]:
                annotations.append(annotation.format(**annotateProperties))
    return annotations

TYPE_ANNOTATIONS = {}
TYPE_ANNOTATIONS['String'] = []
TYPE_ANNOTATIONS['Long'] = []
TYPE_ANNOTATIONS['UUID'] = []
TYPE_ANNOTATIONS['Integer'] = []
TYPE_ANNOTATIONS['String'] = []
TYPE_ANNOTATIONS['Double'] = []
TYPE_ANNOTATIONS['Float'] = []
TYPE_ANNOTATIONS['Timestamp'] = []
TYPE_ANNOTATIONS['Date'] = []
TYPE_ANNOTATIONS['Boolean'] = []
TYPE_ANNOTATIONS['List'] = []

def annotationsForType(javaProperty):
    annotations = []
    javaType = javaProperty.type.split('<')[0].strip()
    if javaType in TYPE_ANNOTATIONS:
        for annotation in TYPE_ANNOTATIONS[javaType]:
            annotations.append(annotation.format(**javaProperty.annotateProperties))
    elif javaType in javaProperty.javaClass.project.models:
        return annotations
    else:
        annotations.append('@Enumerated(EnumType.STRING)')
        annotations.append('@Type(type = "{0}.model.SQLEnumType")'.format(javaProperty.javaClass.project.package))
    return annotations