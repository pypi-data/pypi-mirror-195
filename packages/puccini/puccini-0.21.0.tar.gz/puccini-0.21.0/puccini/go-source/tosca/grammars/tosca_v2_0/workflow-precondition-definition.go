package tosca_v2_0

import (
	"github.com/tliron/puccini/tosca"
)

//
// WorkflowPreconditionDefinition
//
// [TOSCA-v2.0] @ ?
// [TOSCA-Simple-Profile-YAML-v1.3] @ 3.6.26
// [TOSCA-Simple-Profile-YAML-v1.2] @ 3.6.22
// [TOSCA-Simple-Profile-YAML-v1.1] @ 3.5.20
//

type WorkflowPreconditionDefinition struct {
	*Entity `name:"workflow precondition definition"`

	TargetNodeTemplateOrGroupName *string          `read:"target" mandatory:""`
	TargetNodeRequirementName     *string          `read:"target_relationship"`
	ConditionClause               *ConditionClause `read:"condition,ConditionClauseAnd"`

	TargetNodeTemplate *NodeTemplate `lookup:"target,TargetNodeTemplateOrGroupName" traverse:"ignore" json:"-" yaml:"-"`
	TargetGroup        *Group        `lookup:"target,TargetNodeTemplateOrGroupName" traverse:"ignore" json:"-" yaml:"-"`
}

func NewWorkflowPreconditionDefinition(context *tosca.Context) *WorkflowPreconditionDefinition {
	return &WorkflowPreconditionDefinition{Entity: NewEntity(context)}
}

// tosca.Reader signature
func ReadWorkflowPreconditionDefinition(context *tosca.Context) tosca.EntityPtr {
	self := NewWorkflowPreconditionDefinition(context)
	context.ValidateUnsupportedFields(context.ReadFields(self))
	return self
}

//
// WorkflowPreconditionDefinitions
//

type WorkflowPreconditionDefinitions []*WorkflowPreconditionDefinition
